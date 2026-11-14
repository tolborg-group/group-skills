---
name: script
description: Write a new standalone Python script, or change an existing one, for someone still learning Python, in a form they can read, run with uv and edit themselves. Keeps it to a single, well-commented file with its own uv environment, asks what is needed before writing, and explains how to run it. Use when someone asks for a Python script, a small analysis or plotting program, a script to process data files, or a change or fix to such a script, or asks how to run or add a package to one. Not for building Python packages or libraries.
argument-hint: "[what the script should do]"
disable-model-invocation: true
allowed-tools: Bash(uv --version), Bash(uvx ruff format *), Bash(uvx ruff check *)
---

# Write a Python script someone new to Python can own

The person asking is typically a researcher early in their training, perhaps
with a few months of light Python. They need a script they can **read,
understand, run and make small changes to themselves**, not a piece of
software. A shorter, plainer script they understand beats a clever or
"production-ready" one they don't. Every choice below follows from that.

What they asked for, if given: $ARGUMENTS

## 1. Look first

- **Is uv available?** Run `uv --version`. If it is missing, do not install it
  yourself and do not fall back to whatever `python` is on the system. Explain
  in two sentences what uv is (a tool that gives each project its own Python
  and packages, so projects don't interfere with each other) and point them to
  the official installer at https://docs.astral.sh/uv/getting-started/installation/.
  Continue once it is installed.
- **Is there already an environment here?** Look for `pyproject.toml`,
  `uv.lock`, `pixi.toml`, `environment.yml` or `requirements.txt` in the
  folder and its parents.
  - An existing uv project: use it (`uv add`, `uv run`) and don't create
    another one.
  - pixi, conda or something else: use that instead of uv, and say so. Don't
    mix tools in one folder.
  - The folder belongs to someone else's package or a larger codebase: ask
    whether the script belongs there or in its own folder.
- **Is this a change to an existing script?** Then follow "Changing an
  existing script" at the end instead.
- **Where will it live?** A script and its environment belong in their own
  folder (or one folder per group of related scripts). If the current
  directory is their home directory, Desktop or Downloads, suggest making a
  folder first.

## 2. Ask before writing

Ask what you need to know, a few questions at a time, as multiple-choice
questions where your tools allow it. Skip anything already clear from the
request. Typically:

- **What should it do?** In their words, step by step if possible.
- **Input:** which files (format, an example file, where they are), or what
  values.
- **Output:** a plot (saved as a file, which format), a data file, numbers
  printed to the screen?
- **What will they want to vary** between runs? These become the parameters.

Don't ask about things they can't judge yet (code structure, tooling); make a
sensible choice and mention it in the plan.

**Package choices are a chance to learn.** When there is a real choice between
packages, ask, explaining each option in a sentence and saying which you
recommend and why. For example: plain numpy arrays, or pandas as well? Pandas
makes tables with named columns and mixed data easier to work with, but it is
one more library to learn, and numpy alone is enough for columns of numbers.
Only ask when the choice makes a difference to this script; don't invent
choices.

**When a library already does most of the job,** tell them it exists and what
it does. Knowing that is useful in itself. Then ask which they prefer, and
recommend one:

- **Use it directly.** This is usually right when the result matters more than
  learning how it is done, or when the method is easy to get subtly wrong.
- **Write the steps out,** using lower-level building blocks (e.g. numpy and
  `scipy.optimize.curve_fit` instead of a package that fits and plots
  everything in one call). This is better when understanding the method is
  part of the point, as it often is early in a PhD.

Either way, don't write your own version of an established algorithm (fitting,
FFT, integration, reading a standard file format). Use the library for that.
What should be visible in the script is *their* workflow: loading, preparing,
computing, checking and plotting, each as a step they can follow. A script
that is only an import and one function call teaches nothing, so even when a
library does the heavy lifting, show the inputs going in and the result coming
out, and explain in a comment what the call does.

Then give a short plan in plain words and wait for an OK. For example:

> I'll make one file, `fit_spectra.py`, in a new folder `spectra-analysis/`.
> It reads every `.csv` file in `data/`, fits a Gaussian to each spectrum and
> saves a plot `fits.png`. You'll be able to change the input folder and the
> fitting range. It uses numpy, scipy and matplotlib, listed in a
> `pyproject.toml` next to the script.

## 3. Set up the environment

Default: a `pyproject.toml` next to the script. With it, uv puts the
environment in a `.venv/` folder in the project, which editors such as VS Code
pick up automatically, so imports resolve and autocompletion works.

```bash
uv init --bare          # writes a minimal pyproject.toml, nothing else
uv add numpy matplotlib # records the packages and installs them in .venv/
```

`--bare` matters: it does not set the folder up as a package (no `src/`, no
build system, no extra files). Never create a package structure.

**Alternative: inline dependencies** (PEP 723), where the package list lives
in a comment block at the top of the script itself. Offer this only when the
script must travel as a single file (emailed, shared on its own). Tell them the
catch: the editor won't find the environment, so it will underline the imports
in red even though `uv run` works.

```bash
uv init --script analyse.py   # adds the comment block to the script
uv add --script analyse.py numpy
uv lock --script analyse.py   # writes analyse.py.lock with exact versions
```

Packages: stick to the common scientific stack (numpy, scipy, matplotlib,
pandas, and whatever their field uses as standard), as agreed in step 2. Don't
add anything that wasn't in the plan without asking, and prefer the standard
library when it does the job just as plainly (`pathlib`, `csv`, `json`). Every
package is something they will have to understand.

If the folder is a git repository, make sure `.venv/` is in `.gitignore`.

## 4. Write the script

### Shape

One file, read from top to bottom:

1. A module docstring: what the script does, what it reads and writes, and
   how to run it (`uv run script_name.py`).
2. Imports.
3. A few functions, each doing one recognisable step (load, compute, plot,
   save).
4. `main(...)`, which takes the parameters as arguments and calls the steps in
   order.
5. An `if __name__ == "__main__":` block that **defines the parameters** and
   calls `main` with them.

```python
def main(data_dir: Path, temperature: float, output_file: Path) -> None:
    """Run the full analysis: load the data, fit it and save the plot."""
    ...


# This block only runs when the file is run as a script (`uv run fit.py`),
# not when it is imported from another file.
# Change the parameters here.
if __name__ == "__main__":
    data_dir = Path("data")  # folder with the measured spectra (.csv)
    temperature = 300.0  # in kelvin
    output_file = Path("fits.png")

    main(data_dir=data_dir, temperature=temperature, output_file=output_file)
```

Pass the parameters to `main` and on to the functions as arguments. Functions
must never read them as global variables, even though Python would let them.
That keeps each function understandable on its own and makes it easy to turn
the parameters into command-line arguments later.

### Don't

- No package layout, `src/` folder, `setup.py` or several modules.
- No classes unless there is genuinely state to keep together; plain
  functions are easier to follow.
- No `argparse`, click or typer, logging setup, config files, or environment
  variables, unless they asked for them.
- No `try/except` wrapped around everything. Let errors surface with Python's
  own message, which is more useful to them. Check inputs only where a mistake
  is likely and the resulting error would be confusing, and then raise a clear
  message saying what is wrong.
- No absolute paths such as `/Users/...`. Use `pathlib.Path` with paths
  relative to the project folder, or put the path in the parameters.
- No `plt.show()` as the only output; save figures to a file (show as well if
  they want).
- No clever one-liners, nested comprehensions, decorators or other advanced
  idioms where a plain loop reads more clearly.

If the script grows beyond about 200–300 lines, stop and discuss it with them
before continuing: perhaps it is doing too much, or should be split into
steps they run separately.

### Comments, docstrings and type hints

- **Docstrings** on the module and every function: one line on what it does,
  and for anything non-trivial, the arguments and return value with units and
  shapes (NumPy style).
- **Comments explain why and what it means**, not what the Python does: units,
  what each array axis is, where a formula or constant comes from, why a step
  is needed. Don't narrate obvious lines ("# loop over files").
- The exception: Python idioms they may not know yet (`if __name__ ==
  "__main__":`, a list comprehension, `enumerate`, f-strings with format
  specs) get a short comment the first time they appear.
- **Type hints** on function arguments and return values, using built-in types
  (`int`, `float`, `str`, `list[float]`, `dict[str, int]`), `Path`, and the
  types of packages already imported (e.g. `np.ndarray`). Don't import
  anything just for type hints (`typing` constructs, `numpy.typing`), and don't
  use `TypeVar`, `Protocol`, `overload` or similar. Leave a hint out rather
  than write a complicated one.
- Use clear, full variable names (`energies`, not `e`), and the field's
  standard symbols where they are the clearer choice.

### Format and check

After writing, and after every change:

```bash
uvx ruff format script_name.py
uvx ruff check --fix script_name.py
```

Fix anything `ruff check` reports that it could not fix itself. `uvx` runs
ruff without adding it to their project. You don't need to explain ruff
beyond a sentence at hand-over.

## 5. Check that it works

- **If it runs in seconds**, run it yourself with `uv run`, using their input
  files if they're available, or small example inputs you create in a
  temporary folder outside their project. Delete what you created and say
  that you did.
- **If it would take longer**, needs data you don't have, or does anything
  with side effects (overwriting files, large downloads), don't run it. Ask
  them to run it, tell them what they should see when it works, and ask them
  to report back what happened: whether it ran, and whether the result is what
  they wanted. Then fix or adjust.

Never call a script finished just because it looks right.

## 6. Hand it over

Keep it short, as a few small paragraphs or a list:

1. **How to run it:** `uv run script_name.py`, from the project folder, and
   why:
   > `uv run` checks that the project's environment in `.venv/` has exactly
   > the packages in `pyproject.toml` (installing or updating them if not) and
   > runs the script with that environment's Python. You don't have to
   > activate anything or think about which Python is installed, and a
   > colleague who runs the same command gets the same packages.

   Tell them not to use `python script_name.py` or `pip install`: these use
   whichever Python happens to come first on the system, not the project's.
   To add a package later, use `uv add <package>`.
2. **`pyproject.toml` and `uv.lock`**, the first time you create them:
   > `pyproject.toml` lists what the project needs, like "numpy, version 2 or
   > newer". `uv.lock` records the exact versions uv actually installed, down
   > to every package those packages need in turn. The first is the wish
   > list; the lock file is the receipt that lets anyone recreate exactly the
   > same environment later. Keep both, and commit both if you use git.
   > `.venv/` itself can always be recreated, so it is never committed.
3. **A short walkthrough** of the script: what each function does, in order,
   in one line each.
4. **Where to change things:** the parameters in the `if __name__ ==
   "__main__":` block, and what each one does.
5. Optionally, **one small change they could try themselves** (change a
   parameter, add a label to the plot) as a way into the code.

Don't repeat the whole script in the reply; they have the file.

## Changing an existing script

Their script is theirs. Read all of it before changing anything.

- **Keep its structure and style.** Make the smallest change that does what
  they asked. Don't restructure, rename or "clean up" other parts unless they
  ask; if something elsewhere is clearly broken or risky, point it out and ask
  instead of fixing it silently.
- New code follows the conventions above (comments, docstrings, type hints)
  as far as it fits in with the surrounding code.
- **New packages** go in with `uv add <package>` (or
  `uv add --script <file> <package>` for inline dependencies), never by
  hand-editing the dependency list or with `pip install`.
- **No environment yet** (it has been run with a system Python, or they don't
  know how it's run): offer to set one up as in step 3 and explain why in a
  sentence. Don't do it without asking.
- Run ruff only if the script was already formatted with it or they agree:
  reformatting a whole file they know buries the real change.
- Then check it as in step 5, and finish by explaining **what you changed,
  where and why**, briefly, so they can find it in the file.
