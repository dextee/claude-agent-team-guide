"""Exercise install.sh in disposable folders. No network, no Claude calls, no browser."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
AGENTS = sorted(p.name for p in (ROOT / 'agents').glob('*.md'))
PRESET = json.loads((ROOT / 'templates' / 'recommended-settings.json').read_text(encoding='utf-8'))
PRESET.pop('$comment', None)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='claude-guide-test-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.config = self.base / 'isolated-config'

    def run_install(self, *args, expect=0, script=None, path='/usr/bin:/bin', stdin=None):
        env = {**os.environ, 'CLAUDE_CONFIG_DIR': str(self.config), 'HOME': str(self.base)}
        # Hide any real claude binary so the advisory version check stays offline and fast.
        env['PATH'] = path
        cmd = ['bash', '-s', '--', *args] if stdin is not None else ['bash', str(script or ROOT / 'install.sh'), *args]
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=60, input=stdin)
        self.assertEqual(result.returncode, expect, result.stdout + result.stderr)
        return result.stdout + result.stderr

    def write_settings(self, value):
        self.config.mkdir(parents=True, exist_ok=True)
        (self.config / 'settings.json').write_text(json.dumps(value), encoding='utf-8')

    def settings(self):
        return json.loads((self.config / 'settings.json').read_text(encoding='utf-8'))

    def check_agents(self, folder):
        files = sorted(p.name for p in folder.glob('*.md'))
        self.assertEqual(files, AGENTS)
        for name in files:
            self.assertEqual((folder / name).read_bytes(), (ROOT / 'agents' / name).read_bytes())

    def test_replacing_a_linked_agent_preserves_the_other_copy(self):
        agents = self.config / 'agents'
        agents.mkdir(parents=True)
        kept = self.base / 'my-role.md'
        kept.write_bytes(b'My original role')
        os.link(kept, agents / 'worker.md')
        self.run_install()
        self.assertEqual(kept.read_bytes(), b'My original role')
        self.assertEqual((agents / 'worker.md').read_bytes(), (ROOT / 'agents/worker.md').read_bytes())
        self.assertEqual(next(agents.glob('worker.md.bak-*')).read_bytes(), kept.read_bytes())

    def test_dry_run_writes_nothing(self):
        out = self.run_install('--dry-run', '--with-settings')
        self.assertIn('Dry run', out)
        self.assertFalse(self.config.exists())

    def test_default_install_leaves_settings_alone_and_repeats_cleanly(self):
        self.write_settings({'theme': 'dark'})
        before = (self.config / 'settings.json').read_bytes()
        self.run_install()
        self.check_agents(self.config / 'agents')
        self.assertEqual((self.config / 'settings.json').read_bytes(), before)
        out = self.run_install()
        self.assertIn('already up to date', out)
        self.assertFalse(list((self.config / 'agents').glob('*.bak-*')))

    def test_with_settings_merges_and_preserves_existing(self):
        existing = {'theme': 'dark', 'env': {'CUSTOM_FLAG': 'keep',
                                             'CLAUDE_CODE_SUBAGENT_MODEL': 'claude-haiku-5-5'}}
        self.write_settings(existing)
        before = (self.config / 'settings.json').read_bytes()
        out = self.run_install('--with-settings')
        current = self.settings()
        self.assertEqual(current['theme'], 'dark')
        self.assertEqual(current['env']['CUSTOM_FLAG'], 'keep')
        self.assertEqual(current['env']['CLAUDE_CODE_SUBAGENT_MODEL'], 'claude-haiku-5-5')
        self.assertIn('kept', out)
        self.assertNotIn('$comment', current)
        self.assertEqual((self.config / 'settings.json').read_bytes(), before)
        self.assertFalse(list(self.config.glob('settings.json.bak-*')))

    def test_with_settings_on_fresh_config(self):
        self.run_install('--with-settings')
        self.assertEqual(self.settings(), PRESET)

    def test_force_replaces_only_preset_keys(self):
        self.write_settings({'theme': 'dark', 'env': {'CLAUDE_CODE_SUBAGENT_MODEL': 'haiku'}})
        self.run_install('--with-settings', '--force')
        current = self.settings()
        self.assertEqual(current['env']['CLAUDE_CODE_SUBAGENT_MODEL'],
                         PRESET['env']['CLAUDE_CODE_SUBAGENT_MODEL'])
        self.assertEqual(current['theme'], 'dark')

    def test_force_without_settings_is_rejected(self):
        self.run_install('--force', expect=2)

    def test_invalid_settings_json_stops_merge(self):
        self.config.mkdir(parents=True)
        (self.config / 'settings.json').write_text('{not json', encoding='utf-8')
        out = self.run_install('--with-settings', expect=1)
        self.assertIn('not valid JSON', out)
        self.assertEqual((self.config / 'settings.json').read_text(encoding='utf-8'), '{not json')
        self.assertEqual(list(self.config.iterdir()), [self.config / 'settings.json'])

    def test_nonobject_settings_stop_before_creating_agents(self):
        self.write_settings([])
        self.run_install('--with-settings', expect=1)
        self.assertEqual(list(self.config.iterdir()), [self.config / 'settings.json'])
        self.assertEqual(self.settings(), [])

    def test_requested_settings_without_python_fails_before_changes(self):
        tools = self.base / 'tools'
        tools.mkdir()
        for name in ('bash', 'date', 'dirname', 'head', 'grep'):
            (tools / name).symlink_to(Path('/usr/bin') / name)
        out = self.run_install('--with-settings', path=str(tools), expect=1)
        self.assertIn('requires python3', out)
        self.assertFalse(self.config.exists())

    def test_repeated_settings_merge_preserves_only_original_backup(self):
        self.write_settings({'theme': 'keep'})
        original = (self.config / 'settings.json').read_bytes()
        self.run_install('--with-settings')
        self.run_install('--with-settings')
        backups = list(self.config.glob('settings.json.bak-*'))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_bytes(), original)

    def test_two_agent_backups_survive_the_same_timestamp(self):
        tools = self.base / 'tools'
        tools.mkdir()
        clock = tools / 'date'
        clock.write_text('#!/bin/sh\necho 20000101-000000\n')
        clock.chmod(0o755)
        agents = self.config / 'agents'
        agents.mkdir(parents=True)
        for text in ('first custom copy', 'second custom copy'):
            (agents / 'worker.md').write_text(text)
            self.run_install(path=f'{tools}:/usr/bin:/bin')
        self.assertEqual(sorted(p.read_text() for p in agents.glob('worker.md.bak-*')),
                         ['first custom copy', 'second custom copy'])

    def test_identical_unowned_agent_survives_before_and_after_install(self):
        agents = self.config / 'agents'
        agents.mkdir(parents=True)
        personal = agents / 'worker.md'
        personal.write_bytes((ROOT / 'agents' / personal.name).read_bytes())
        self.run_install('--uninstall')
        self.assertTrue(personal.is_file())
        self.run_install()
        self.run_install()
        self.run_install('--uninstall')
        self.assertEqual(list(agents.iterdir()), [personal])

    def test_offline_uninstall_uses_manifest_for_retired_role(self):
        self.run_install()
        agents = self.config / 'agents'
        (agents / 'worker.md').rename(agents / 'archivist.md')
        manifest = agents / '.agent-team-manifest'
        manifest.write_text(manifest.read_text().replace('worker.md', 'archivist.md'))
        # No adjacent source files and no network access.
        standalone = self.base / 'uninstall.sh'
        standalone.write_bytes((ROOT / 'install.sh').read_bytes())
        tools = self.base / 'tools'
        tools.mkdir()
        curl = tools / 'curl'
        curl.write_text('#!/bin/sh\nexit 1\n')
        curl.chmod(0o755)
        self.run_install('--uninstall', script=standalone, path=f'{tools}:/usr/bin:/bin')
        self.assertEqual(list(agents.iterdir()), [])

    def test_rejects_invalid_manifest_before_removing_owned_siblings(self):
        self.run_install()
        agents = self.config / 'agents'
        manifest = agents / '.agent-team-manifest'
        with manifest.open('a') as out:
            out.write('0' * 64 + '  ../other.md\n')
        self.run_install('--uninstall', expect=1)
        self.check_agents(agents)

    def test_manifest_symlink_is_refused_before_install_or_uninstall(self):
        agents = self.config / 'agents'
        agents.mkdir(parents=True)
        outside = self.base / 'personal.txt'
        outside.write_text('leave this alone')
        (agents / '.agent-team-manifest').symlink_to(outside)
        for args in ((), ('--uninstall',)):
            self.run_install(*args, expect=1)
        self.assertEqual(outside.read_text(), 'leave this alone')
        self.assertFalse(list(agents.glob('*.md')))

    def test_project_install_backs_up_changed_agent(self):
        project = self.base / 'project with spaces'
        agents = project / '.claude' / 'agents'
        agents.mkdir(parents=True)
        (agents / 'implementer.md').write_text('original custom agent', encoding='utf-8')
        self.run_install('--project', str(project))
        self.check_agents(agents)
        backup = next(agents.glob('implementer.md.bak-*'))
        self.assertEqual(backup.read_text(encoding='utf-8'), 'original custom agent')
        self.assertFalse(self.config.exists())

    def test_symlinked_agent_file_is_not_followed(self):
        agents = self.config / 'agents'
        agents.mkdir(parents=True)
        outside = self.base / 'outside.md'
        outside.write_text('do not overwrite', encoding='utf-8')
        (agents / 'architect.md').symlink_to(outside)
        out = self.run_install()
        self.assertIn('symlink', out)
        self.assertEqual(outside.read_text(encoding='utf-8'), 'do not overwrite')

    def test_symlinked_agents_folder_is_refused(self):
        real = self.base / 'elsewhere'
        real.mkdir()
        self.config.mkdir(parents=True)
        (self.config / 'agents').symlink_to(real, target_is_directory=True)
        self.run_install(expect=1)
        self.assertEqual(list(real.iterdir()), [])

    def test_uninstall_keeps_edited_files(self):
        self.run_install()
        edited = self.config / 'agents' / 'editor.md'
        edited.write_text('my changes', encoding='utf-8')
        out = self.run_install('--uninstall')
        remaining = sorted(p.name for p in (self.config / 'agents').glob('*.md'))
        self.assertEqual(remaining, ['editor.md'])
        self.assertIn('kept', out)

    def test_dry_run_over_existing_files_changes_nothing(self):
        self.write_settings({'env': {'CLAUDE_CODE_SUBAGENT_MODEL': 'haiku'}})
        agents = self.config / 'agents'
        agents.mkdir()
        (agents / 'worker.md').write_text('custom worker', encoding='utf-8')
        before = {p.name: p.read_bytes() for p in self.config.rglob('*') if p.is_file()}
        self.run_install('--dry-run', '--with-settings', '--force')
        after = {p.name: p.read_bytes() for p in self.config.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_uninstall_after_release_change_uses_manifest(self):
        self.run_install()
        manifest = self.config / 'agents' / '.agent-team-manifest'
        self.assertEqual(len(manifest.read_text(encoding='utf-8').splitlines()), len(AGENTS))
        # Simulate a newer release whose explorer differs from the installed copy.
        newer = self.base / 'newer'
        (newer / 'agents').mkdir(parents=True)
        (newer / 'templates').mkdir()
        for name in AGENTS:
            text = (ROOT / 'agents' / name).read_text(encoding='utf-8')
            if name == 'explorer.md':
                text += '\nA line added in a later release.\n'
            (newer / 'agents' / name).write_text(text, encoding='utf-8')
        (newer / 'templates' / 'recommended-settings.json').write_bytes(
            (ROOT / 'templates' / 'recommended-settings.json').read_bytes())
        (newer / 'install.sh').write_bytes((ROOT / 'install.sh').read_bytes())
        out = self.run_install('--uninstall', script=newer / 'install.sh')
        self.assertEqual(list((self.config / 'agents').glob('*.md')), [], out)
        self.assertFalse(manifest.exists())

    def test_piped_install_downloads_through_curl(self):
        # A stub curl copies files from this checkout, so no network is used.
        stub_bin = self.base / 'bin'
        stub_bin.mkdir()
        curl = stub_bin / 'curl'
        curl.write_text(
            '#!/bin/bash\n'
            'url=""; out=""\n'
            'while [ $# -gt 0 ]; do case "$1" in -o) out="$2"; shift;; -*) ;; *) url="$1";; esac; shift; done\n'
            f'cp "{ROOT}/${{url#*/main/}}" "$out"\n', encoding='utf-8')
        curl.chmod(0o755)
        script = (ROOT / 'install.sh').read_text(encoding='utf-8')
        out = self.run_install(stdin=script, path=f'{stub_bin}:/usr/bin:/bin')
        self.assertIn('Downloading', out)
        self.check_agents(self.config / 'agents')


if __name__ == '__main__':
    unittest.main(verbosity=2)
