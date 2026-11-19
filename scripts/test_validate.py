"""Regression tests for scripts/validate.py. Pure text checks: no network, no model calls."""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate as v  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding='utf-8')


class CostAndRateChecks(unittest.TestCase):
    def setUp(self):
        self.models = read('docs/models-and-effort.md')
        self.cost = read('docs/cost-and-evaluation.md')
        self.readme = read('README.md')

    def test_published_documents_reconcile(self):
        self.assertEqual(v.check_rates_and_costs(self.models, self.cost, self.readme), [])

    def test_rejects_wrong_displayed_total(self):
        changed = self.cost.replace('| $0.080 |', '| $0.800 |')
        self.assertNotEqual(changed, self.cost)
        errors = v.check_rates_and_costs(self.models, changed, self.readme)
        self.assertTrue(any('displayed total' in e for e in errors), errors)

    def test_rejects_rate_drift_from_models_json(self):
        changed = self.models.replace('| `claude-opus-5-5` | $4.00 |', '| `claude-opus-5-5` | $5.00 |')
        self.assertNotEqual(changed, self.models)
        errors = v.check_rates_and_costs(changed, self.cost, self.readme)
        self.assertTrue(any('rates differ' in e for e in errors), errors)

    def test_rejects_cost_row_using_old_rates(self):
        changed = self.cost.replace('| Fable 5.2 | 10,000 / 1M × $8.00 | 2,000 / 1M × $40.00 | $0.160 |',
                                    '| Fable 5.2 | 10,000 / 1M × $10.00 | 2,000 / 1M × $50.00 | $0.200 |')
        self.assertNotEqual(changed, self.cost)
        errors = v.check_rates_and_costs(self.models, changed, self.readme)
        self.assertTrue(any('Fable 5.2 rates differ' in e for e in errors), errors)

    def test_models_json_change_is_caught_in_docs(self):
        data = json.loads(json.dumps(v.MODEL_DATA))
        data['current'][0]['input_usd_per_mtok'] = '9.00'
        errors = v.check_rates_and_costs(self.models, self.cost, self.readme, data)
        self.assertTrue(any('templates/models.json' in e for e in errors), errors)

    def test_rejects_readme_price_drift(self):
        changed = self.readme.replace('| $2 / $10 |', '| $3 / $15 |')
        self.assertNotEqual(changed, self.readme)
        errors = v.check_rates_and_costs(self.models, self.cost, changed)
        self.assertTrue(any('README: Sonnet 5.5 price' in e for e in errors), errors)

    def test_rejects_readme_fable_price_from_previous_model(self):
        changed = self.readme.replace('| $8 / $40 |', '| $10 / $50 |')
        self.assertNotEqual(changed, self.readme)
        errors = v.check_rates_and_costs(self.models, self.cost, changed)
        self.assertTrue(any('README: Fable 5.2 price' in e for e in errors), errors)

    def test_rejects_token_counts_that_disagree_with_prose(self):
        changed = self.cost.replace('| Haiku 5.5 | 10,000 /', '| Haiku 5.5 | 20,000 /')
        self.assertNotEqual(changed, self.cost)
        errors = v.check_rates_and_costs(self.models, changed, self.readme)
        self.assertTrue(any('token counts differ' in e for e in errors), errors)

    def test_rejects_duplicate_rate_row(self):
        row = next(l for l in self.models.splitlines() if l.startswith('| `claude-haiku-5-5`'))
        changed = self.models.replace(row, row + '\n' + row)
        errors = v.check_rates_and_costs(changed, self.cost, self.readme)
        self.assertTrue(any('duplicate' in e for e in errors), errors)


class AgentChecks(unittest.TestCase):
    def setUp(self):
        self.text = read('agents/reviewer.md')

    def test_published_agent_passes(self):
        self.assertEqual(v.check_agent(self.text, 'reviewer'), [])

    def test_rejects_retired_or_unknown_model(self):
        changed = self.text.replace('model: claude-sonnet-5-5', 'model: claude-sonnet-5')
        self.assertTrue(any('not a current model' in e for e in v.check_agent(changed, 'reviewer')))

    def test_rejects_missing_tools(self):
        changed = self.text.replace('tools: Read, Glob, Grep, Bash\n', '')
        self.assertTrue(any('"tools"' in e for e in v.check_agent(changed, 'reviewer')))

    def test_rejects_bad_effort_and_name_mismatch(self):
        changed = self.text.replace('effort: high', 'effort: ultra')
        errors = v.check_agent(changed, 'auditor')
        self.assertTrue(any('effort' in e for e in errors))
        self.assertTrue(any('does not match' in e for e in errors))

    def test_rejects_previous_fable_in_agent_file(self):
        text = read('agents/auditor.md').replace('model: claude-fable-5-2', 'model: claude-fable-5-1')
        self.assertTrue(any('not a current model' in e for e in v.check_agent(text, 'auditor')))

    def test_rejects_misspelled_frontmatter_field(self):
        text = read('agents/worker.md').replace('maxTurns: 40', 'maxturns: 40')
        errors = v.check_agent(text, 'worker')
        self.assertTrue(any('"maxturns" is not a documented frontmatter field' in e for e in errors), errors)

    def test_rejects_bad_field_values(self):
        worker = read('agents/worker.md')
        cases = [
            (worker.replace('isolation: worktree', 'isolation: container'), 'isolation must be'),
            (worker.replace('maxTurns: 40', 'maxTurns: forty'), 'maxTurns must be'),
            (worker.replace('color: green', 'color: magenta'), 'color "magenta"'),
            (read('agents/explorer.md').replace('omitClaudeMd: true', 'omitClaudeMd: yes please'), 'omitClaudeMd must be'),
        ]
        for text, expected in cases:
            stem = 'explorer' if 'omitClaudeMd' in text and 'name: explorer' in text else 'worker'
            errors = v.check_agent(text, stem)
            self.assertTrue(any(expected in e for e in errors), (expected, errors))

    def test_rejects_bad_names(self):
        for bad in ('-reviewer', 'agent-team:reviewer', 'r' * 257):
            text = self.text.replace('name: reviewer', f'name: {bad}')
            self.assertTrue(any('cannot contain' in e for e in v.check_agent(text, bad)), bad)

    @unittest.skipIf(v.yaml is None, 'PyYAML not installed')
    def test_yaml_cross_parse_catches_invalid_yaml(self):
        text = self.text.replace('description: Routine', 'description: [Routine')
        errors = v.check_agent(text, 'reviewer')
        self.assertTrue(any('not valid YAML' in e for e in errors), errors)

    @unittest.skipIf(v.yaml is None, 'PyYAML not installed')
    def test_yaml_cross_parse_checks_types(self):
        text = read('agents/worker.md').replace('maxTurns: 40', 'maxTurns: "40"')
        errors = v.check_agent(text, 'worker')
        self.assertTrue(any('maxTurns' in e for e in errors), errors)

    def test_rejects_agent_tool(self):
        changed = self.text.replace('tools: Read, Glob, Grep, Bash', 'tools: Read, Agent')
        self.assertTrue(any('spawn' in e for e in v.check_agent(changed, 'reviewer')))

    def test_readme_table_must_match_files(self):
        readme = read('README.md')
        agents = {n: v.parse_frontmatter(read(f'agents/{n}.md'))[0] for n in v.AGENT_NAMES}
        self.assertEqual(v.check_readme_agents(readme, agents), [])
        agents['worker'] = {**agents['worker'], 'effort': 'high'}
        self.assertTrue(v.check_readme_agents(readme, agents))


class ConsistencyChecks(unittest.TestCase):
    def setUp(self):
        self.agents = {n: v.parse_frontmatter(read(f'agents/{n}.md'))[0] for n in v.AGENT_NAMES}

    def test_agents_doc_matches_files(self):
        doc = read('docs/agents.md')
        self.assertEqual(v.check_agents_doc(doc, self.agents), [])
        changed = doc.replace('| Haiku 5.5 / medium | Read, Glob, Grep |', '| Haiku 5.5 / low | Read, Glob, Grep |')
        self.assertNotEqual(changed, doc)
        self.assertTrue(v.check_agents_doc(changed, self.agents))

    def test_min_version_drift_is_caught(self):
        readme = read('README.md')
        self.assertEqual(v.check_min_version({'README.md': readme}, '2.1.321'), [])
        self.assertTrue(v.check_min_version({'README.md': readme}, '2.1.293'))

    def test_team_minimum_follows_the_pinned_models(self):
        self.assertEqual(v.team_min_version(self.agents), '2.1.321')
        downgraded = {**self.agents, 'architect': {**self.agents['architect'], 'model': 'claude-opus-5-5'},
                      'auditor': {**self.agents['auditor'], 'model': 'claude-opus-5-5'}}
        self.assertEqual(v.team_min_version(downgraded), '2.1.293')

    def test_installer_matches_team_minimum(self):
        import re
        installer = read('install.sh')
        self.assertEqual(re.search(r'MIN_VERSION="([\d.]+)"', installer).group(1), v.team_min_version(self.agents))


class HygieneChecks(unittest.TestCase):
    def test_flags_leftover_marker(self):
        marker = 'TO' + 'DO'
        self.assertTrue(v.check_text_hygiene(f'Fix this {marker}: later', 'x.md'))

    def test_flags_credential_and_unexpected_email(self):
        token = 'sk-ant-' + 'a' * 30
        self.assertTrue(v.check_text_hygiene(f'key={token}', 'x.md'))
        self.assertTrue(v.check_text_hygiene('mail someone@' + 'company.test now', 'x.md'))
        self.assertEqual(v.check_text_hygiene('dextee@users.noreply.github.com', 'x.md'), [])

    def test_flags_hype_outside_code(self):
        self.assertTrue(v.check_hype('A revolutionary guide.', 'x.md'))
        self.assertEqual(v.check_hype('```\nrevolutionary\n```\n', 'x.md'), [])


class NewDocChecks(unittest.TestCase):
    def test_raw_refs(self):
        ok = 'curl https://raw.githubusercontent.com/dextee/claude-agent-team-guide/main/install.sh'
        sha = 'https://raw.githubusercontent.com/dextee/claude-agent-team-guide/' + 'a' * 40 + '/install.sh'
        base = 'https://raw.githubusercontent.com/dextee/claude-agent-team-guide/'
        tag = base + 'v2.0.0/install.sh'
        self.assertEqual(v.check_raw_refs(ok + ' ' + sha, 'x.md'), [])
        self.assertTrue(v.check_raw_refs(tag, 'x.md'))
        release = json.loads(read('.claude-plugin/plugin.json'))['version']
        self.assertEqual(v.check_raw_refs(base + 'v' + release + '/install.sh', 'x.md'), [])
        self.assertEqual(v.check_raw_refs(read('SETUP.md'), 'SETUP.md'), [])

    def test_unknown_model_names(self):
        self.assertEqual(v.check_model_names('Fable 5.2, Fable 5.1, Opus 5.5 and Haiku 4.5', 'x.md'), [])
        invented = 'Fable ' + '5.' + '5'
        self.assertTrue(v.check_model_names(f'Use {invented} for audits.', 'x.md'))
        self.assertTrue(v.check_model_names('Haiku 6 is fast.', 'x.md'))

    def test_docs_footer(self):
        good = 'Body\n\n*Independent guide, not an Anthropic publication; product facts checked 2026-11-15.*\n'
        self.assertEqual(v.check_docs_footer(good, 'x.md', '2026-11-15', True), [])
        self.assertTrue(v.check_docs_footer('Body only\n', 'x.md', '2026-11-15', True))
        self.assertTrue(v.check_docs_footer(good, 'x.md', '2026-12-01', True))
        self.assertEqual(v.check_docs_footer(good, 'x.md', '2026-12-01', False), [])

    def test_every_docs_page_has_footer(self):
        for path in sorted((ROOT / 'docs').rglob('*.md')):
            rel = path.relative_to(ROOT).as_posix()
            if rel in v.FOOTER_EXEMPT:
                continue
            self.assertEqual(v.check_docs_footer(path.read_text(encoding='utf-8'), rel, v.CHECKED_ON,
                                                 not rel.startswith('docs/atlas/')), [], rel)

    def test_recipes_need_prompt_and_proof(self):
        recipes = read('docs/workflows.md')
        self.assertEqual(v.check_sections(recipes, 'w', r'## (?=\d)', v.EXPECTED_RECIPES), [])
        first = recipes.index(v.PROOF_LINE)
        broken = recipes[:first] + recipes[first:].replace(v.PROOF_LINE, '**Done means:**', 1)
        self.assertTrue(any('What proves it worked' in e for e in v.check_sections(broken, 'w', r'## (?=\d)', v.EXPECTED_RECIPES)))

    def test_patterns_need_prompt_and_proof(self):
        patterns = read('docs/orchestration-patterns.md')
        self.assertEqual(v.check_sections(patterns, 'p', r'## Pattern ', v.EXPECTED_PATTERNS), [])
        broken = patterns.replace('```text', '```', 1)
        self.assertTrue(any('copy-paste prompt' in e for e in v.check_sections(broken, 'p', r'## Pattern ', v.EXPECTED_PATTERNS)))


@unittest.skipIf(shutil.which('jq') is None, 'jq not installed')
class HookTemplateChecks(unittest.TestCase):
    GATE = ROOT / 'templates' / 'hooks' / 'subagent-stop-gate.sh'

    def run_gate(self, payload):
        return subprocess.run(['bash', str(self.GATE)], input=json.dumps(payload), text=True,
                              capture_output=True, timeout=30)

    def test_gate_blocks_report_without_contract(self):
        r = self.run_gate({'stop_hook_active': False, 'last_assistant_message': 'All done, tests pass.'})
        self.assertEqual(r.returncode, 2, r.stderr)
        self.assertIn('STATUS', r.stderr)

    def test_gate_passes_report_with_contract(self):
        msg = 'STATUS: done\nRESULT: fixed\nCHECKS RUN:\n- pytest -> 0 -> 12 passed'
        r = self.run_gate({'stop_hook_active': False, 'last_assistant_message': msg})
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_gate_does_not_loop(self):
        r = self.run_gate({'stop_hook_active': True, 'last_assistant_message': 'no contract'})
        self.assertEqual(r.returncode, 0, r.stderr)


class AnchorChecks(unittest.TestCase):
    def test_github_style_slugs(self):
        self.assertEqual(v.slugify('The Quartet: map, plan, build, prove'), 'the-quartet-map-plan-build-prove')
        self.assertEqual(v.slugify('Effort: start at the default, escalate on evidence'),
                         'effort-start-at-the-default-escalate-on-evidence')

    def test_headings_inside_code_are_ignored(self):
        self.assertNotIn('not-a-heading', v.headings('```\n# Not a heading\n```\n# Real\n'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
