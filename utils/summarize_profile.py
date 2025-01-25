import json
import os
import sys

# Get the paths of various python paths, keeping track of the ones that are likely to hold source code.
python_core_paths = {}
for next_path in sys.path:
    if next_path.endswith(f"{os.sep}site-packages") or next_path.endswith(
        f"{os.sep}Lib"
    ):
        last_separator_index = next_path.rfind(os.sep)
        python_core_paths[next_path] = "{python}" + next_path[last_separator_index:]

# Get the path of the pymarkdown project, to shorten some of the paths we see.
base_project_path = os.path.join(os.getcwd(), "pymarkdown") + os.sep


## Read in the file.
with open(sys.argv[1], "r", encoding="utf-8") as stats_input_file:
    stats_input_lines = stats_input_file.readlines()

# The stats fill has some prefix and suffix to the following lines, but it is these lines we are looking for:
#
# ncalls    tottime  percall  cumtime  percall filename:lineno(function)
# 1600       25.554    0.016   54.422    0.034 C:\enlistments\pymarkdown\pymarkdown\container_blocks\container_block_processor.py:318(__look_back_in_document_for_block_quote)
# 58246318   16.601    0.000   23.959    0.000 C:\enlistments\pymarkdown\pymarkdown\tokens\markdown_token.py:250(is_block_quote_start)
have_seen_header_row = False
eligible_lines = []
for next_line in stats_input_lines:
    next_line = next_line.strip()
    if next_line.startswith("ncalls "):
        have_seen_header_row = True
    elif have_seen_header_row:
        if not next_line:
            break
        eligible_lines.append([x for x in next_line.split(" ") if x.strip()])

# With the eligible lines isolated, add the first two columns as is, and try and strip down the "path" as much as possible
# into file_name, line_number, and function_name.
curated_samples = []
for next_line in eligible_lines:
    curated_row = {"ncalls": next_line[0], "tottime": next_line[1]}
    if len(next_line) > 6:
        curated_file_name = " ".join(next_line[5:])
        curated_line_number = "N/A"
        curated_function_name = "N/A"
    else:
        if next_line[5].startswith(base_project_path):
            curated_file_name = next_line[5][len(base_project_path) :]
        else:
            curated_file_name = next(
                (
                    dde + next_line[5][len(ddd) :]
                    for ddd, dde in python_core_paths.items()
                    if next_line[5].startswith(ddd)
                ),
                next_line[5],
            )
        file_name_end_index = curated_file_name.index(":")
        curated_line_number = curated_file_name[file_name_end_index + 1 :]
        line_number_end_index = curated_line_number.index("(")
        curated_function_name = curated_line_number[line_number_end_index + 1 : -1]
        curated_line_number = curated_line_number[:line_number_end_index]
        curated_file_name = curated_file_name[:file_name_end_index]
    curated_row["file_name"] = curated_file_name
    curated_row["line_number"] = curated_line_number
    curated_row["function_name"] = curated_function_name
    curated_samples.append(curated_row)

print(json.dumps(curated_samples))
