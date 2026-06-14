#!/usr/bin/env python3
"""Script to remove shellcheck hooks from .pre-commit-config.yaml and save to fred.yaml."""

import sys
from typing import List

import yaml


def __remove_shellcheck_repos(
    input_file: str, output_file: str, id_to_remove: str
) -> None:
    """Remove repos containing shellcheck hooks from input YAML and write to output."""
    with open(input_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if not config or "repos" not in config:
        print("No repos found in the configuration file.")
        return

    filtered_repos: List[str] = []
    for repo in config["repos"]:
        if "hooks" not in repo:
            filtered_repos.append(repo)
            continue

        if filtered_hooks := [
            hook for hook in repo["hooks"] if hook.get("id") != id_to_remove
        ]:
            repo_copy = repo.copy()
            repo_copy["hooks"] = filtered_hooks
            filtered_repos.append(repo_copy)

    config["repos"] = filtered_repos

    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(
            config,
            f,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )

    print(f"Successfully wrote {output_file} without shellcheck hooks.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(sys.argv)
        sys.exit(1)
    __remove_shellcheck_repos(".pre-commit-config.yaml", sys.argv[1], "shellcheck")
