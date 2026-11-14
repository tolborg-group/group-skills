# Group skills

Shared skills for Claude Code (and other tools that support the
[Agent Skills](https://agentskills.io) standard), organised as a Claude Code
plugin marketplace.

## Skills

| Skill                      | What it does                                                         |
|----------------------------|----------------------------------------------------------------------|
| `/git:sync`                | Commits, pulls and pushes to get a repo up to date, explaining each git command |
| `/reading:paper-interview` | Questions you about a paper, like a fair examiner, to test your understanding   |
| `/latex:diagnose`          | Finds out why a LaTeX document does not compile and fixes it                    |
| `/writing:draft-critique`  | Critiques your draft one issue at a time, as a conversation                     |
| `/python:script`           | Writes or changes a readable, well-commented Python script, run with uv         |

Each skill lives in a plugin (`git`, `reading`, `writing`, `latex`, `python`) that is installed
separately. Claude also picks a skill up on its own when you describe the
task, e.g. "quiz me on this paper".

## Install

In a terminal:

```bash
claude plugin marketplace add tolborg-group/group-skills
claude plugin install git@tolborg-group
claude plugin install reading@tolborg-group
claude plugin install writing@tolborg-group
claude plugin install latex@tolborg-group
claude plugin install python@tolborg-group
```

Or, inside Claude Code, run `/plugin` and browse the marketplace.

## Update

Updates are not automatic by default. Either run
`claude plugin update git@tolborg-group` (once per plugin), or turn on
auto-update for this marketplace under **Marketplaces** in `/plugin`.

Project templates can declare these plugins so they are set up automatically;
see [docs/using-in-a-template.md](docs/using-in-a-template.md).

## Layout

```
.claude-plugin/marketplace.json    lists every plugin in this repo
plugins/<plugin>/
  .claude-plugin/plugin.json       plugin manifest
  skills/<skill>/SKILL.md          one folder per skill
templates/SKILL.md                 starting point for a new skill
tests/                             scenario tests (run on demand)
tools/validate.py                  checks manifests and skills (runs in CI)
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
