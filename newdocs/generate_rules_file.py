"""
Quick and dirty script to create the "rules.md" file from components
of the extensions files themselves.
"""

import os
import shutil
import tempfile

script_path = os.path.dirname(os.path.realpath(__file__))
extensions_path = os.path.join(script_path, "src", "plugins")
extension_files = os.listdir(extensions_path)
extension_files.sort()

with tempfile.NamedTemporaryFile() as temp_output:
    temporary_file_name = temp_output.name
with open(temporary_file_name, "wt", encoding="utf-8") as destination_file:
    destination_file.write("# Rules\n")

    for next_extension_file in extension_files:
        with open(
            os.path.join(extensions_path, next_extension_file), "r", encoding="utf-8"
        ) as readme_file:
            file_contents = readme_file.read()

            first_prefix = "# "
            assert file_contents.startswith(first_prefix)
            dd = file_contents.index("\n")
            extension_title_text = file_contents[len(first_prefix) : dd]

            end_of_first_part = file_contents.index("\n## Reasoning")
            replacement_text = (
                file_contents[dd:end_of_first_part]
                .replace(
                    "## Summary",
                    "<!-- pyml disable-next-line no-duplicate-heading-->\n### Summary",
                )
                .replace(
                    "## Deprecation",
                    "<!-- pyml disable-next-line no-duplicate-heading-->\n### Deprecation",
                )
                .replace("./rule_", "./plugins/rule_")
            )
            while replacement_text.startswith("\n"):
                replacement_text = replacement_text[1:]

            destination_file.write(
                f"""\n## {extension_title_text}

[Full Documentation](./plugins/{next_extension_file})

{replacement_text}"""
            )
print(temporary_file_name)

output_path = os.path.join(script_path, "src", "rules.md")
shutil.copyfile(temporary_file_name, output_path)

# rule_md033/
