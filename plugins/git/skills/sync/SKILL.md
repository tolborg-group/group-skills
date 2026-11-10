---
name: sync
description: Bring a git repository up to date in both directions, saving local changes as a commit, pulling what others have pushed and pushing the result, while briefly explaining each git command so the user learns them. Use when someone asks to sync, update, save, upload, pull or push their work with git or GitHub, or is unsure which git commands they need.
argument-hint: "[commit message]"
allowed-tools: Bash(git status *), Bash(git log *), Bash(git diff *), Bash(git fetch *)
---

# Sync a repository and teach the commands

The user wants their repository up to date: their local work saved and shared,
and other people's work brought in. Most people using this are researchers who
use git occasionally and do not have the commands memorised. Do the work for
them, and leave them a little more able to do it themselves next time.

Commit message from the user, if any: $ARGUMENTS

## Look first

Find out where things stand before changing anything: `git status`, the
current branch and whether it tracks a remote branch, then `git fetch` and how
many commits the branch is ahead and behind. Check for an operation left
half-finished (a merge, rebase or cherry-pick in progress).

Tell the user what you found in plain words, for example: "You have changed
three files and not saved them yet, and two new commits from others are on
GitHub." Then say what you are going to do about it.

## Do it, one step at a time

Only the steps the situation needs, normally in this order:

1. **Commit local changes.** Show which files will be included. Use the
   user's message if they gave one, otherwise write a short one that says what
   changed and tell them what it is.
2. **Pull.** Follow the repository's own configuration or documented
   convention if there is one. Otherwise merge (`git pull --no-rebase`), which
   is easier to follow and to undo for someone new to git.
3. **Push.** If the branch has no upstream yet, set it with `git push -u`.

Ask before committing when it is not obvious that everything belongs in the
commit: files that look like secrets or credentials, large data or binary
files, build output, or changes that look unrelated to each other. Suggest
`.gitignore` for things that should never be committed. Ask before pushing if
the user only asked to save or to update, not to share.

If there is nothing to do, say so; that is a fine outcome.

## Teaching

For each command that changes something, say in one sentence what it does and
why it is needed now, and show the exact command you ran. Explain in terms of
what happens to their work ("this records your changes as a snapshot on your
machine; nothing has left your computer yet"), not in git's internal terms.

Keep it short. One sentence per command, no lectures, and do not explain
commands you did not need. If the user clearly knows git already, drop the
explanations and just report.

Finish with the commands they could have typed themselves, in order, as a
copyable block, with a one-line note on anything unusual that happened.

## When it is not straightforward

- **Merge conflict.** Stop and explain that git could not combine two changes
  to the same lines. For each conflict show both versions and what each side
  was trying to do. Resolve mechanical conflicts yourself and say how; for
  anything where the content matters (text, parameters, results), ask which
  version the user wants. Never pick a side silently. They can always back
  out with `git merge --abort`.
- **Unfinished merge or rebase from before.** Explain what state the
  repository is in and ask whether to finish it or abort it.
- **Push rejected.** Usually someone pushed in the meantime: pull again, then
  push. If the branch is protected, explain that the change needs a pull
  request and offer to open one.
- **Detached HEAD, no remote, or not on the expected branch.** Explain what it
  means and ask what the user intended before acting.
- **Authentication failure.** You cannot fix this from here. Say what failed
  and what the user needs to set up.

## Limits

Never run commands that can destroy work unless the user asks for that
specific thing after you have explained what will be lost: force pushes,
`git reset --hard`, `git clean`, `git checkout -- <file>` or `git restore`
over uncommitted changes, deleting branches, or rewriting commits that have
been pushed. If the only way forward seems to need one of these, stop and
explain the situation instead.
