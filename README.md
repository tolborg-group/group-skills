# Group skills

Shared skills for Claude Code (and other tools that support the
[Agent Skills](https://agentskills.io) standard), organised as a Claude Code
plugin marketplace.

## Plugins

| Plugin    | What it is for                                              |
|-----------|-------------------------------------------------------------|
| `git`     | Saving and sharing work with git, teaching the commands     |
| `reading` | Reading papers, e.g. an examiner-style interview            |
| `latex`   | LaTeX help, e.g. diagnosing compilation errors              |

Skills are invoked as `/plugin:skill`, e.g. `/git:sync`.

## Install

In a terminal:

```bash
claude plugin marketplace add tolborg-group/group-skills
claude plugin install git@tolborg-group
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
