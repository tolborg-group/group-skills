# Using these plugins in a project template

## 1. Declare the plugins in the template

Commit `.claude/settings.json` to the template, enabling only the plugins that
fit it:

```json
{
  "extraKnownMarketplaces": {
    "tolborg-group": {
      "source": { "source": "github", "repo": "tolborg-group/group-skills" }
    }
  },
  "enabledPlugins": {
    "git@tolborg-group": true,
    "reading@tolborg-group": true,
    "writing@tolborg-group": true,
    "latex@tolborg-group": true
  },
  "permissions": {
    "deny": [
      "Bash(git push --force *)",
      "Bash(git push -f *)",
      "Bash(git reset --hard *)"
    ]
  }
}
```

The `deny` rules are the hard limits. A skill's `allowed-tools` only
pre-approves commands; it cannot block anything.

Skills that only make sense for one project stay in that template's own
`.claude/skills/`.

## 2. Optional: pixi tasks

Claude Code is meant to prompt for installing declared plugins when a folder
is trusted, but this has been unreliable, so an explicit setup task is a
useful fallback:

```toml
[tasks.check-claude]
cmd = "claude --version > /dev/null || (echo \"Claude Code not found. Install it and run 'claude' once to log in.\" && exit 1)"

[tasks.setup-claude]
depends-on = ["check-claude"]
cmd = "claude plugin marketplace add tolborg-group/group-skills && claude plugin install git@tolborg-group && claude plugin install reading@tolborg-group && claude plugin install writing@tolborg-group && claude plugin install latex@tolborg-group"
```

Once skills exist, a launcher task can start one directly, e.g.
`cmd = 'claude "/git:sync"'` (plugin skills are invoked as `/plugin:skill`).

Keep each `cmd` on one line: pixi's shell rejects a line that starts with
`||` or `&&`.
