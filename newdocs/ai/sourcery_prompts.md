# Sourcery Prompts

## Documentation

To scan each document listed below, apply each step in order as a sourcery prompt. This entails looking
for the text between the starting fenced code block (with 6 `\`` characters) and the ending
of the same fenced code block. Any additional instructions are specified as a list
of items at the start of each step.

### General Files

**GOAL:** To get these documents scanning to a level of 17/20 or higher.
**TARGET AUDIENCE:** Unless stated, new users of PyMarkdown

#### Determine if the open file can be entirely seen in the context window

- depending on the density of the text, context window can be anywhere between
  200 and 500 lines

``````text
what is the name of the open file, and what are the last 10 lines you see of the open file?
``````

- If the file does not fit in the context window, determine a heading before the last line as shown in that output where the text logically splits into another section.  Treat the beginning of the file to that point as slice 1.  Then repeat this process with the rest of the file to break it up into slices.
- Otherwise, use general steps below.  These have been applied to:
    - `newdocs/src/index.md`
    - `newdocs/src/usual.md`
    - `newdocs/src/quick-starts/*.md`
    - `README.md`

#### Step 1: Analyze File

``````text
As a reader that is new to using the PyMarkdown project, rate the readability of the open file on a scale from 0 to 25. explain your readability score with clear details backed with a numeric score.  Do not evaluate any text that is contained within a table.

Suggested areas to focus on are:
- Overall structure and navigation
- Concept clarity and progression
- Language, style, and precision
- Example quality with explanations and integration into document
- Audience Awareness and Onboarding for new users
Rate each one of these areas with a score from 0 to 5.
``````

#### Step 2: Pick A Specific Issue to Focus On Improving

- Replace `<issue>` with the issue text, as presented in an improvements-like section of the readability rating report.

``````text
explain each instance of behavior that you found and labelled "<issue>". for each instance of that behavior that occurs, offer 2 concrete examples on how to fix it
``````

### Files: `newdocs/src/contribute.md`, `newdocs/src/advanced_configuration.md`, `newdocs/src/advanced_extensions.md`, `newdocs/src/advanced_pre-commit.md`, `newdocs/src/advanced_plugins.md`

**GOAL:** To get each slice scanning to a level of 17/20 or higher.
**TARGET AUDIENCE:** Experienced users of PyMarkdown

<!-- pyml disable-next-line no-duplicate-heading-->
#### Step 1: Analyze File

``````text
As a reader that is relatively experienced with the PyMarkdown project and understands how things work, rate the readability of the open file on a scale from 0 to 25. explain your readability score with clear details backed with a numeric score.  Do not evaluate any text that is contained within a table.

Suggested areas to focus on are:
- Overall structure and navigation
- Concept clarity and progression
- Language, style, and precision
- Example quality and integration
- Cross-referencing and context for experienced users
Rate each one of these areas with a score from 0 to 5.
``````

<!-- pyml disable-next-line no-duplicate-heading-->
#### Step 2: Pick A Specific Issue to Focus On Improving

- Replace `<issue>` with the issue text, as presented in an improvements-like section of the readability rating report.

``````text
explain each instance of behavior that you found and labelled "<issue>". for each instance of that behavior that occurs, offer 2 concrete examples on how to fix it
``````

### Files: `newdocs/src/quick-starts/advanced.md`

**GOAL:** To get each slice scanning to a level of 17/20 or higher.
**TARGET AUDIENCE:** Experienced users of PyMarkdown who are also experienced systems people.

<!-- pyml disable-next-line no-duplicate-heading-->
#### Step 1: Analyze File

``````text
As a reader that is experienced with Python, Python package managers like Pipenv, and the Pre-Commit tool, rate the readability of the open file on a scale from 0 to 25. explain your readability score with clear details backed with a numeric score.

Suggested areas to focus on are:
- Overall structure and navigation
- Concept clarity and progression
- Language, style, and precision
- Example quality and integration
- Cross-referencing with other documents and usage by experienced Python users
Rate each one of these areas with a score from 0 to 5.
``````

<!-- pyml disable-next-line no-duplicate-heading-->
#### Step 2: Pick A Specific Issue to Focus On Improving

- Replace `<issue>` with the issue text, as presented in an improvements-like section of the readability rating report.

``````text
explain each instance of behavior that you found and labelled "<issue>". for each instance of that behavior that occurs, offer 2 concrete examples on how to fix it
``````

### File: `newdocs/src/getting-started.md`

**GOAL:** To get each slice scanning to a level of 17/20 or higher.
**TARGET AUDIENCE:** Experienced users of PyMarkdown

#### Step 1: Define Slices

``````text
for the file `getting-started.md`:
assume the first slice is from the start of the file to the line "## CI/CD Pipelines".
the second slice is from the line `## CI/CD Pipelines` to the end of the file.
``````

#### Step 2: Paste Content

- Replace `<file contents>` with the contents of the file.

``````text
the contents of `getting-started.md` are as follows:
````
<file contents>
````
``````

#### Step 3: Analyze Slices

``````text
For each slice:
    As a reader that is relatively experienced with the PyMarkdown project and understands how things work, rate the readability of the open file on a scale from 0 to 25. explain your readability score with clear details backed with a numeric score.  Do not evaluate any text that is contained within a table.

    Suggested areas to focus on are:
    - Overall structure and navigation
    - Concept clarity and progression
    - Language, style, and precision
    - Example quality and integration
    - Cross-referencing and context for experienced users
    Rate each one of these areas with a score from 0 to 5.
When done with all slices, show the readability numbers for each slice
``````

#### Step 4: Pick A Specific Issue to Focus On Improving

- Replace `<slice>` with the slice containing the issue(s) to examine.
- Replace `<issue>` with the exact issue label or summary as it appears in the "Improvements" (or "Issues") section of the readability rating report.

``````text
in slice <slice>, explain each instance of behavior that you found and labelled "<issue>". for each instance of that behavior that occurs, offer 2 concrete examples on how to fix it
``````

### File: `newdocs/src/user-guide.md`

**GOAL:** To get these slices scanning to a level of 17/20 or higher.
**TARGET AUDIENCE:** Experienced users of PyMarkdown

#### Step 1: Define Slices

``````text
For the file `user-guide.md`:

- The first slice is from the start of the file to the line `## Command Line Basics`.
- The second slice is from the line `## Command Line Basics` to `### Basic Scanning`.
- The third slice is from the line `### Basic Scanning` to `### Advanced Scanning`.
- The fourth slice is from the line `### Advanced Scanning` to `### Basic Fixing`.
- The fifth slice is from the line `### Basic Fixing` to the line `### Extensions`.
- The sixth slice is from the line `### Extensions` to the line `### Plugin Rules`.
- The seventh slice is from the line `### Plugin Rules` to the line `### Basic Configuration`.
- The eighth slice is from the line `### Basic Configuration` to the line `### Information Commands`.
- The ninth slice is from the line `### Information Commands` to the end of the file.
``````

#### Step 2: Paste Content

- Replace `<file contents>` with the contents of the file.

``````text
the contents of `user-guide.md` are as follows:
````
<file contents>
````
``````

#### Step 3: Analyze Slices

``````text
For each slice:
    As a reader that is relatively experienced with the PyMarkdown project and understands how things work, rate the readability of the open file on a scale from 0 to 25. explain your readability score with clear details backed with a numeric score.  Do not evaluate any text that is contained within a table.

    Suggested areas to focus on are:
    - Overall structure and navigation
    - Concept clarity and progression
    - Language, style, and precision
    - Example quality and integration
    - Cross-referencing and context for experienced users
    Rate each one of these areas with a score from 0 to 5.
When done with all slices, show the readability numbers for each slice
``````

#### Step 4a: Pick Something General to Focus On Improving

- Replace `<slice>` with the slice containing the issue(s) to examine.

``````text
for each issue that you raised in slice <slice>, clearly describe each issue, include the text before the change, the text after the change, and two suggestions on how to mitigate the issue
``````

#### Step 4b: Pick A Specific Issue to Focus On Improving

- Replace `<slice>` with the slice containing the issue(s) to examine.
- Replace `<issue>` with the issue text, as presented in an improvements-like section of the readability rating report.

``````text
in slice <slice>, explain each instance of behavior that you found and labelled "<issue>". for each instance of that behavior that occurs, offer 2 concrete examples on how to fix it
``````

## checks

- ensure caps are followed properly
    - `Quick Start guides`
    - `Pragma` or `Pragmas`
    - `Rule Engine`
    - `Front-Matter` or `Front-Matter blocks`
    - `Markdown token stream`
    - `md0`xx -> `MD0`xx
    - `autofix` -> `**autofix** capability`
    - `scan mode` -> `**scan** mode`
    - `fix mode` -> `**fix** mode`
    - `violations` -> `failures`
    - `failures` -> `Rule Failures`
    - `ids` or `primary ids` or `primary identifiers` -> `Rule ID`
    - `alter` + `ids` or `identifiers` --> aliases

    - `rules` are for the logic
    - `Rule Plugins` are for the container i.e. you diable the Rule Plugin

- remove unicode
    - `’` --> `'`
    - `“` --> `"`
    - `”` --> `"`
    - `—` --> `&mdash;`

### Covered & rechecked Files

- `newdocs/src/quick-starts/advanced.md`
- `newdocs/src/quick-starts/extensions.md`
- `newdocs/src/quick-starts/fixing.md`
- `newdocs/src/quick-starts/general.md`
- `newdocs/src/quick-starts/index.md`
- `newdocs/src/quick-starts/installation.md`
- `newdocs/src/quick-starts/rules.md`
- `newdocs/src/quick-starts/scanning.md`
- `newdocs/src/advanced_configuration.md`
- `newdocs/src/advanced_extensions.md`
- `newdocs/src/advanced_plugins.md`
- `newdocs/src/advanced_pre-commit.md`
- `newdocs/src/contribute.md`
- `newdocs/src/index.md`
- `newdocs/src/usual.md`

- `newdocs/src/getting-started.md`
- `newdocs/src/user-guide.md`

### Requiring Final Read and Link Check

- make sure pypi points to new docs, not old docs

### Remaining Files

api
development

extensions/*
plugins/*
api/*

- create a lexicon?
- add a couple of FAQs containing concepts like rule vs Rule Plugin, and when used?
- in quick-starts, add more links to where those topics are?  only at start?


“Lead‑in sentences under each major heading” are short, 1–2 sentence paragraphs placed immediately after a heading that:

state the purpose of the section, and
give readers a quick mental model before they see details.
They help scanning readers decide “Do I need this section?” without committing to a full read, and they clarify how the section fits into the rest of the page.

explain more about "Improvement 1: Add short lead‑in sentences under each major heading" and give 2 examples for each major heading



4. Section Transitions Could Be Slightly Sharper
Behavior
The high‑level sections are logically ordered:

Basic Integration
Advanced Integration
How We Use Pre‑Commit in our Pipelines
Things To Watch Out For
However, transitions between them are sometimes implicit, making it slightly harder for a skimmer to understand “why this next section exists”.
