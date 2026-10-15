"""Regression tests for scripts/validate.py. Pure text checks: no network, no model calls."""
from pathlib import Path
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

    def test_rejects_rate_drift_between_documents(self):
        changed = self.models.replace('| `claude-opus-5-5` | $4.00 |', '| `claude-opus-5-5` | $5.00 |')
        self.assertNotEqual(changed, self.models)
        errors = v.check_rates_and_costs(changed, self.cost, self.readme)
        self.assertTrue(any('rates differ' in e for e in errors), errors)

    def test_rejects_readme_price_drift(self):
        changed = self.readme.replace('$2 / $10 |', '$3 / $15 |')
        self.assertNotEqual(changed, self.readme)
        errors = v.check_rates_and_costs(self.models, self.cost, changed)
        self.assertTrue(any('README: Sonnet 5.5 price' in e for e in errors), errors)

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
        self.assertEqual(v.check_min_version({'README.md': readme}, '2.1.293'), [])
        self.assertTrue(v.check_min_version({'README.md': readme}, '2.1.300'))


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


class AnchorChecks(unittest.TestCase):
    def test_github_style_slugs(self):
        self.assertEqual(v.slugify('The Quartet: map, plan, build, prove'), 'the-quartet-map-plan-build-prove')
        self.assertEqual(v.slugify('Effort: start at the default, escalate on evidence'),
                         'effort-start-at-the-default-escalate-on-evidence')

    def test_headings_inside_code_are_ignored(self):
        self.assertNotIn('not-a-heading', v.headings('```\n# Not a heading\n```\n# Real\n'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
