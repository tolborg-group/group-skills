# Contributing

Anyone in the group can add or improve a skill. Changes go through a pull
request, because skills directly control what Claude does in everyone's
repositories.

## Adding a skill

1. Pick the plugin it belongs in. If none fits, create a new one: a folder
   under `plugins/` with a `.claude-plugin/plugin.json`, plus an entry in
   `.claude-plugin/marketplace.json`.
2. Copy `templates/SKILL.md` to `plugins/<plugin>/skills/<skill-name>/SKILL.md`.
   The folder name and the `name` field must match.
3. Write the skill, then run `python tools/validate.py`.
4. Try it locally (see below), then open a pull request.

## Writing a good skill

- **The description decides when the skill is used.** Claude only sees the
  name and description until the skill is loaded, so say what it does and
  name the situations that should trigger it.
- **Keep it portable.** Stick to standard instructions so the skill also works
  in other tools. Claude Code-specific frontmatter (`allowed-tools`,
  `disable-model-invocation`, `argument-hint`) is fine; other tools ignore it.
- **Side effects:** for skills that change things (commits, pushes, files),
  consider `disable-model-invocation: true` so they only run when typed.
- **`allowed-tools` pre-approves, it does not restrict.** Hard limits belong in
  `permissions.deny` in a project's `.claude/settings.json`.
- **Watch out for `!` followed by a backtick.** In Claude Code that runs a
  shell command when the skill loads, even inside code blocks. The validator
  warns about it.
- Keep `SKILL.md` under about 500 lines; put long reference material in
  separate files in the skill folder and link to them.

## Trying a skill locally

Point Claude Code at your working copy instead of GitHub:

```bash
claude plugin marketplace add ./path/to/group-skills
```

## Versioning

The `plugin.json` files deliberately have no `version` field. Without one,
Claude Code uses the git commit as the version, so every merged change reaches
people the next time they update. Do not add a `version`: a fixed version
number that nobody remembers to bump keeps everyone on the old copy.
