"""
Module to quickly determine if a Pipfile.lock file is older than its parent Pipfile.

Used in clean.cmd.
"""
import os
import sys

if not os.path.exists("Pipfile"):
    print("Pipfile not present. Raising alert.")
    sys.exit(2)

if not os.path.exists("Pipfile.lock"):
    print("Lock file not present. Regenerating.")
    sys.exit(1)

pipfile_time = os.path.getmtime("Pipfile")
lockfile_time = os.path.getmtime("Pipfile.lock")
if pipfile_time > lockfile_time:
    print("Pipfile is newer than lock file. Regenerating.")
    sys.exit(1)

sys.exit(0)
