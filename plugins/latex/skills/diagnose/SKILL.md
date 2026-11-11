---
name: diagnose
description: Diagnose why a LaTeX document fails to compile, by reading the log, finding the real cause in the source and fixing it. Use when a LaTeX build fails, a PDF is not produced or comes out wrong, or the user pastes a LaTeX error such as "Undefined control sequence", "Missing $ inserted", "Runaway argument" or "File not found".
argument-hint: "[main .tex file or pasted error]"
---

# Diagnose a LaTeX compilation failure

The user has a LaTeX document that does not compile and wants to know why and
get it building again. LaTeX error messages often name a symptom far from the
cause, so the work is mostly in tracing the message back to the source.

What the user gave: $ARGUMENTS

## Get a fresh, complete log

Find the main file and how the project is built: a `latexmkrc`, a Makefile, a
task in `pixi.toml` or similar, or a `% !TEX` line at the top of the file. Use
the project's own build command when there is one, so you get the same engine
(pdflatex, xelatex, lualatex) and bibliography tool (bibtex, biber) the user
gets. Otherwise:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex
```

Compile it yourself instead of trusting a `.log` already on disk, which may be
from an older run. If LaTeX is not installed here (the user may work on
Overleaf), work from the log or error text they give you and say that you
could not compile to confirm.

## Find the first real error

Start from the first error in the log. Later errors are usually consequences
of the first and disappear once it is fixed, so do not report them as a list
of separate problems.

Read the surrounding lines, not only the line starting with an
exclamation mark. The lines
after it show the text LaTeX was reading when it stopped, broken at the exact
position. The log wraps at 79 characters, so file names and messages can be
split across lines. The open parentheses before the error tell you which file
was being read.

Then open the source at that place and read around it. Things that commonly
mislead:

- **The reported line is where LaTeX noticed, not where the mistake is.** An
  unclosed brace or environment, or a missing `$`, is reported at the end of
  the paragraph, at the next environment, or at the end of the file. Look
  backwards from the reported line.
- **An error inside a generated file** (`.aux`, `.toc`, `.bbl`, `.out`) means
  the cause is in the source that wrote it: a caption, section title or
  bibliography entry, often with a fragile command or a special character
  such as `_`, `&` or `%`.
- **Stale auxiliary files.** After a failed run they can keep producing errors
  even when the source is fixed. If an error makes no sense or survives a
  correct fix, clean them (`latexmk -c`) and compile again.
- **Wrong engine.** `fontspec` and `unicode-math` need xelatex or lualatex;
  some older packages need pdflatex.
- **Bibliography.** Errors from biber or bibtex are in the `.blg` file, not
  the `.log`. Running bibtex on a document set up for biber, or the reverse,
  gives empty citations without a LaTeX error.
- **Missing package or file.** Check spelling and path first, then whether the
  package is installed in this TeX distribution.

Undefined references and citations are warnings that need another run or a
bibliography run. They are not the reason a build fails, though latexmk may
report them at the end.

If the log does not localise the problem, bisect: compile with half of the
content or half of the `\input` files left out and narrow it down. Do this on
a copy or revert it afterwards.

## Explain, fix, confirm

Tell the user what was wrong in a sentence or two: what LaTeX was complaining
about, and what in their source caused it, with file and line. Explain the
message itself briefly when it is cryptic, since they will meet it again.

Fix it when the fix is mechanical and has one sensible form: a missing brace,
a misspelled command, an unescaped character, a missing `\usepackage`. Ask
first when the fix involves a choice about their document, such as which
package to use, changing the engine or the document class, or rewording
content.

Compile again after each fix and continue with the next first error until the
build succeeds. Say plainly at the end whether it now compiles, and list what
you changed.

Do not make the error go away without fixing it. Do not delete or comment out
the user's content to get a PDF, do not switch to `batchmode` or
`scrollmode` to run past errors, and do not replace their packages or class
with something simpler. If the only fix you can find removes something they
wrote, stop and describe the problem to them.

Leave warnings such as overfull boxes alone unless the user asks about them.
