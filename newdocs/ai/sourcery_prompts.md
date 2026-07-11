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

``````text
As a reader that has 2-3 years of Python experience, is experienced with the PyMarkdown project, and understands how things work, rate the readability of the open file on a scale from 0 to 25. explain your readability score with clear details backed with a numeric score.  Do not evaluate any text that is contained within a table.

Suggested areas to focus on are:
- Overall structure and navigation
- Concept clarity and progression
- Language, style, and precision
- Example quality with explanations and integration into document
- Audience Awareness and Onboarding for new users
Rate each one of these areas with a score from 0 to 5.
`````

## xxxx

`````prompt
# Role
Act as a senior technical writer and usability expert reviewing documentation for the `application_properties` project.

# Task
Evaluate the open file. Your audience is a software developer with 3-5 years of experience with Python,
thorough experience with using PyMarkdown from the command line.
Rate its readability on a scale of 0–50 based on 5 distinct categories (0–10 points each).
If providing any fenced code blocks with markdown in them, ensure that the fenced code block is constructed with five ~ characters, as it may contain suggested text that includes its own code blocks.

# Evaluation Criteria
You must evaluate the following 5 areas. For each area, provide a score (0-10) and analysis:
1. **Overall Structure and Navigation**
2. **Concept Clarity and Progression**
3. **Language, Style, and Precision** (Critical: Specifically check for run-on sentences that need breaking up)
4. **Example Quality** (Check for explanations and integration into the document)
5. **Audience Awareness and Onboarding**

## Fix Importance:
-  each weakness is assigned an integer between 1 and 5 signifying how important it is to fix that weakness.
- a 1 is a trivial fix that is more of a light recommendation, while a 5 is a weakness that will typically drop that sections score by at least 3 points

# Output Format Requirements
You must follow this EXACT output structure. Do not add introductory or concluding remarks outside of this format.

## Section 1: Summary Scorecard
- Present a markdown table with the following columns: `Category`, `Score (0-10)`.
- At the bottom of the table, include a row for `TOTAL SCORE` out of 50.

```
| Category | Score |
| :--- | :--- |
| Overall Structure and Navigation | [Score] |
| Concept Clarity and Progression | [Score] |
| Language, Style, and Precision | [Score] |
| Example Quality | [Score] |
| Audience Awareness and Onboarding | [Score] |
| **TOTAL SCORE** | **[Total]** |
```

## Section 2: Detailed Analysis
Below the table, provide a detailed breakdown for each category in the order listed above. Use the following **exact** sub-structure for EACH category:

```
### [Category Name]: [Score]/10

**Strengths**
1. **[4-5 word title]:** [1-3 sentences explaining the strength and how it contributed to the score].
2. **[4-5 word title]:** [1-3 sentences explaining the strength and how it contributed to the score].
*(Repeat for all strengths found)*

**Weaknesses**
1. **[4-5 word title] | Fix Importance: [1-5]/5**: [1-2 sentence summary of the core issue].
   - *Specific Examples:*
     - [Example 1: Quote specific text or describe specific pattern]
     - [Example 2: Quote specific text or describe specific pattern]
     - [Example 3: Quote specific text or describe specific pattern]
   - *(Repeat for all examples found)*
   - *Impact:* [1 sentence on how this negatively impacted the score/reader experience]
*(Repeat for all weaknesses found)*
```

# Analysis Constraints

- Ensure all [Category Name] headings match the 5 categories listed in the Evaluation Criteria exactly.
- Ensure all strength titles are no more than 4-5 words long.
- Ensure all weakness lines include the `Fix Importance: [N]` integer inline.
- For the "Language, Style, and Precision" category, explicitly mention any long sentences that should be broken up in the Weaknesses section if applicable.
- **Crucial:** If a weakness category contains multiple distinct issues (e.g., spelling, grammar, run-on sentences), you MUST use the nested list format above to enumerate them clearly. Do not cram multiple distinct errors into a single prose sentence. Use bullet points for each distinct example.
- **Crucial:** All references to other sections within the same document must be hyperlinked.
- **STRICT ANCHOR CONSTRAINT:** Do not critique, suggest, or report on anchor consistency, heading normalization, or link fragility. These are validated by the project's linting script.
- **Scope boundary:** Do not suggest or critique the presence/absence of a Table of Contents (it is auto-generated).
- If the document contains cross-references to anchors, assume they are functionally perfect and out of scope. 

# Never Do These Things

- Never critique, suggest, or report on anchor consistency, heading normalization, or link fragility. These are validated by the project's linting script.
- Never complain about any weaknesses regarding any of the following items, as these are all verified by the project's linting script:
  - anchors and links
  - fragile links to anchors of other sections in the current or other documents
- Never complain about a Python practice that a competent intermediate Python developer with 3 years of experience would know.
`````

## xxx

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

extensions/*
plugins/*

- create a lexicon?
- add a couple of FAQs containing concepts like rule vs Rule Plugin, and when used?
- in quick-starts, add more links to where those topics are?  only at start?


```prompt
for the docstring comment for the `scan_path` method in the `pymarkdown\api.py` file, determine each way that the writing could be improved.  For each way found, provide the existing text, what the issue is with the docstring, and 2-3 concrete recommendations on how to address the issue.

DO NOT:
- do not raise any issues regarding parameters missing type information. that information is already provided by the mkdocstring configuration.
- do not raise any issues regarding the mixing of plaintext and markdown in the content.  that is already checked by mkdocs and mkdocstrings
```

```prompt
in the file `pymarkdown\api.py`, verify that the docstrings of the following methods are structurally and stylistically consistent with each other:
- `list_path`
- `scan_path`
- `fix_path`
- `scan_string`
- `fix_string`
analyze each of the docstrings sections for consistency.  if a section is consistent, simply output the name of the section and `consistent`.  otherwise, output the name of the section and why it is not consistent with concrete information on why it is not consistent.
```

```prompt
in the file `pymarkdown\api.py`, first look at the examples sections in the docstrings for each of the `list_path`, `scan_path` and `fix_path` methods as well as the examples section in the PyMArkdownApi class.
1. list the name of the method and the names of the examples for that method
2. one a scale of 1 to 5 (where 5 is highest) rate the cohesion of the examples as a group. assume that the order they are presented in the rendered documentation is `list_path`, `scan_path`, `fix_path`. if the rating is not 5, provide solid explanations on why the rating is not 5 along with concrete examples of how to raise the rating. take into account that it is intentional that the first example for each method is a snippet to show its part of the workflow identified in the class example.
```

```prompt
in the file `pymarkdown\api.py`, verify that the docstrings of the following methods  are structurally and stylistically consistent with each other:
- `disable_rule_by_identifier`
- `enable_rule_by_identifier`
- `enable_extension_by_identifier`
- `configuration_file_path`
- `set_boolean_property`
- `set_integer_property`
- `set_string_property`
- `set_property`
- `enable_strict_configuration`
- `log_debug_and_above`
- `log_info_and_above`
- `log_warning_and_above`
- `log_error_and_above`
- `log_critical_and_above`
- `log`
- `log_to_file`
- `add_plugin_path`
- `enable_stack_trace`
- `disable_json5_configuration`
- `enable_continue_on_error`
analyze each of the docstrings sections for consistency.  if a section is consistent, simply output the name of the section and `consistent`.  otherwise, output the name of the section and why it is not consistent with concrete information on why it is not consistent.
```

```
in the file `pymarkdown\api.py`, analyze the docstrings of the following methods for spelling and grammar mistakes:
- `disable_rule_by_identifier`
- `enable_rule_by_identifier`
- `enable_extension_by_identifier`
- `configuration_file_path`
- `set_boolean_property`
- `set_integer_property`
- `set_string_property`
- `set_property`
- `enable_strict_configuration`
- `log_debug_and_above`
- `log_info_and_above`
- `log_warning_and_above`
- `log_error_and_above`
- `log_critical_and_above`
- `log`
- `log_to_file`
- `add_plugin_path`
- `enable_stack_trace`
- `disable_json5_configuration`
- `enable_continue_on_error`
for grammar mistakes, provide 2-3 recommendations on how to fix the mistake, including how the recommendation improves the grammar.
```

```
in the file `pymarkdown\api.py`, analyze the docstrings of the following classes for spelling and grammar mistakes:
- `PyMarkdownScanFailure`
- `PyMarkdownPragmaError`
- `PyMarkdownScanPathResult`
- `PyMarkdownFixResult`
- `PyMarkdownFixStringResult`
for grammar mistakes, provide 2-3 recommendations on how to fix the mistake, including how the recommendation improves the grammar.
```
