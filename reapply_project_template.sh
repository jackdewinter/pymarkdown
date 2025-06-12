#!/usr/bin/env bash

# Set the script mode to "strict".
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ without the fail fast.
set -uo pipefail

# Set up any project based local script variables.
SCRIPT_NAME=$(basename -- "${BASH_SOURCE[0]}")
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

# Give the user hints on how the script can be used.
show_usage() {
	echo "Usage:"
	echo "  ${SCRIPT_NAME} [flags]"
	echo ""
	echo "Summary:"
	echo "  Reapply the templating used to create the project, if required."
	echo ""
	echo "Flags:"
	echo "  -g,--generate           Generate default configuration file."
	echo "  -l,--list               List mode."
	echo "  -f,--force              Force the template to be re-applied, even if synced."
	echo "  -v,--verbose            Verbose mode."
	echo "  -x,--debug              Display debug information about the script as it executes."
	echo "  -h,--help               Display this help text."
	echo ""
	exit 1
}

# Parse the command line.
parse_command_line() {

	VERBOSE_MODE=0
	FORCE_MODE=
	LIST_MODE=
	GENERATE_MODE=
	DEBUG_MODE=0
	PARAMS=()
	while (("$#")); do
		case "$1" in
		-g | --generate)
			GENERATE_MODE=--generate-config
			shift
			;;
		-l | --list)
			LIST_MODE=--list
			shift
			;;
		-f | --force)
			FORCE_MODE=-f
			shift
			;;
		-v | --verbose)
			VERBOSE_MODE=1
			shift
			;;
		-x | --debug)
			DEBUG_MODE=1
			shift
			;;
		-h | --help)
			show_usage
			;;
		-*) # unsupported flags
			echo "Error: Unsupported flag ${1}" >&2
			show_usage
			;;
		*) # preserve positional arguments
			PARAMS+=("${1}")
			shift
			;;
		esac
	done

	if [[ ${DEBUG_MODE} -ne 0 ]]; then
		set -x
	fi
}

verbose_echo() {
	echo_text=${1:-}

	if [ "${VERBOSE_MODE}" -ne 0 ]; then
		echo "${echo_text}"
	fi
}

load_properties_from_file() {

	verbose_echo "{Loading 'project.properties file'...}"
	while IFS='=' read -r key_value; do
		if [[ ${key_value} == \#* ]]; then
			continue
		fi
		key=$(echo "${key_value}" | cut -d '=' -f1)
		value=$(echo "${key_value}" | cut -d '=' -f2-)
		export "${key}=${value}"
	done <"${SCRIPT_DIR}/project.properties"

	if [[ -z ${PYTHON_MODULE_NAME} ]]; then
		complete_process 1 "Property 'PYTHON_MODULE_NAME' must be defined in the project.properties file."
	fi
}

# Parse any command line values.
parse_command_line "$@"

load_properties_from_file

# Main body of the script.

echo "ADD WARNING TO MAKE SURE ALL FILES COMMITTTED BEFORE, ASK FOR YES, EXPLAIN WHY"

# rem Capture the Hashes for the two Pipfiles before any changes.
# @For /F Delims^= %%G In ('""%__AppDir__%certutil.exe" -HashFile "Pipfile"|"%__AppDir__%find.exe" /V ":""')Do @Set "PIPFILE_SHA1=%%G"

if [[ ${VERBOSE_MODE} -ne 0 ]]; then
	echo "{Applying re-template operation to project.}"
fi

echo "{Applying template.}"
if ! pipenv run cookieslicer --output-directory . --source-directory /c/enlistments/template/libraries ${LIST_MODE} ${FORCE_MODE} ${GENERATE_MODE} --project-name "${PYTHON_MODULE_NAME}"; then
	echo ""
	echo "{Applying template to existing directory failed.}"
	exit 1
fi

# rem Capture the Hashes for the two Pipfiles after any changes.
# @For /F Delims^= %%G In ('""%__AppDir__%certutil.exe" -HashFile "Pipfile"|"%__AppDir__%find.exe" /V ":""')Do @Set "NEW_PIPFILE_SHA1=%%G"

if [[ ${VERBOSE_MODE} -ne 0 ]]; then
	echo "{PipFile hash before !PIPFILE_SHA1! and after !NEW_PIPFILE_SHA1!.}"
fi
# if not [!PIPFILE_SHA1!] == [!NEW_PIPFILE_SHA1!] (
#     goto need_sync
# )

if [[ ${VERBOSE_MODE} -ne 0 ]]; then
	echo "{Pipfile hash has not changed.  Recreation and resync of packages not required.}"
fi
# goto success_end

# :need_sync
# echo {Pipfile hashes have changed.  Recreation and resync of packages required.}
# echo {Please exit any open instances of VSCode before pressing a key.}
# echo {Failure to exit any such Python instances will cause the recreate and resync to fail.}
# timeout /t -1

if [[ ${VERBOSE_MODE} -ne 0 ]]; then
	echo "{Clearing old lock file and virtual environment.}"
fi
# erase Pipfile.lock
# pipenv --rm

if [[ ${VERBOSE_MODE} -ne 0 ]]; then
	echo "{Creating new lock file and virtual environment.}"
fi
# pipenv lock
# pipenv sync -d

exit 0
