# Tests

Scenario tests for skills go here, one folder per plugin (e.g. `tests/git/`).

The idea: set up a throwaway situation (e.g. a sandbox git repo with a local
"remote"), run the skill headless with `claude -p`, and assert on the outcome
(repository state, commands in the transcript) rather than on wording.
Results are not deterministic, so run each scenario a few times.

These cost API usage, so they run on demand, not on every push.
