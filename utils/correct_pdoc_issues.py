import os
import subprocess
import sys

# This is the file we expect to be changed, so make sure it is not there to start.
expected_file_path = os.path.join("docs", "api.md")
os.remove(expected_file_path)

# Run PDoc to cause the documentation to be generated.
pdoc_args = ["pdoc", "-o", "docs", "--force", "pymarkdown/api.py"]
run_result: subprocess.CompletedProcess = subprocess.run(
    pdoc_args, stdout=subprocess.PIPE
)
if run_result.returncode:
    print(f"PDoc returned non-zero error code ({run_result.returncode}).")
    sys.exit(1)

# The output should be a single line with the file we expected to be
# changed. Cause noise if it is anything but.
resultant_stdout = run_result.stdout.decode("utf-8").replace("\r", "").strip("\n")
split_stdout = resultant_stdout.split("\n")
if len(split_stdout) != 1:
    print("BAD2")
    sys.exit(1)
if split_stdout[0] != expected_file_path:
    print("BAD3")
    sys.exit(1)
if not os.path.exists(expected_file_path):
    print("BAD4")
    sys.exit(1)

# Read the file in...
with open(expected_file_path, encoding="utf-8") as file_to_parse:
    file_as_lines = file_to_parse.readlines()

# Make sure that the second line are "=" for a SetExt header, and insert
# a newline after them...
if file_as_lines[1][0] != "=":
    print("BAD5")
    sys.exit(1)
file_as_lines[0] = f"# {file_as_lines[0]}"
file_as_lines[1] = "\n"

# rt = file_as_lines.index("#### Parameters\n")
# file_as_lines.insert(rt, "<!-- pyml disable-next-line header-increment-->\n")

rt = file_as_lines.index("Classes\n")
assert rt != -1
file_as_lines[rt] = f"## {file_as_lines[rt]}"
del file_as_lines[rt + 1]

for j, i in enumerate(file_as_lines):
    x = i
    if x and x[-1] == "\n":
        x = x[:-1]
    y = x.rstrip()
    if y != x:
        # print(f"{j}>{x}<>{y}<")
        file_as_lines[j] = f"{y}\n"

# If the file does not end in a newline, add one...
if file_as_lines[-1]:
    file_as_lines.append("\n")

# And write the changes back out.
with open(expected_file_path, "wt", encoding="utf-8") as file_to_write:
    file_to_write.writelines(file_as_lines)
