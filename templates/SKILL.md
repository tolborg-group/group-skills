---
name: skill-name
description: What the skill does AND when to use it. Claude decides whether to load the skill from this text alone, so name the situations and phrases that should trigger it.
# Optional fields (Claude Code specific; other tools ignore them):
# argument-hint: "<required> [optional]"
# disable-model-invocation: true   # only runs when typed as a /command
# allowed-tools: Bash(git status *)  # pre-approves tools; does NOT restrict
---

# Title

Instructions for Claude, written as you would brief a capable colleague.

User input passed after the command is available as: $ARGUMENTS
