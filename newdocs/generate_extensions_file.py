"""
Quick and dirty script to create the "extensions.md" file from components
of the extensions files themselves.
"""

import os
import shutil
import tempfile

script_path = os.path.dirname(os.path.realpath(__file__))
extensions_path = os.path.join(script_path, "src", "extensions")
extension_files = os.listdir(extensions_path)
extension_files.sort()

with tempfile.NamedTemporaryFile() as temp_output:
    temporary_file_name = temp_output.name
with open(temporary_file_name, "wt", encoding="utf-8") as destination_file:
    destination_file.write("# Extensions\n")

    for next_extension_file in extension_files:
        with open(
            os.path.join(extensions_path, next_extension_file), "r", encoding="utf-8"
        ) as readme_file:
            file_contents = readme_file.read()

            first_prefix = "# "
            assert file_contents.startswith(first_prefix)
            end_of_first_part = file_contents.index("\n")
            extension_title_text = file_contents[len(first_prefix) : end_of_first_part]

            second_prefix = "\n## Summary\n"
            start_of_second_part = file_contents.index(second_prefix) + len(
                second_prefix
            )
            end_of_second_part = file_contents.index("\n## ", start_of_second_part)
            extension_summary_text = file_contents[
                start_of_second_part:end_of_second_part
            ]
            destination_file.write(
                f"""\n## {extension_title_text}

[Full Documentation](./extensions/{next_extension_file})

<!--- pyml disable-next-line no-duplicate-heading-->
### Summary
{extension_summary_text}"""
            )
print(temporary_file_name)

output_path = os.path.join(script_path, "src", "extensions.md")
shutil.copyfile(temporary_file_name, output_path)
