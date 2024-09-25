import shutil
import subprocess
import sys

MINIMUM_COMMITIZEN_VERSION = '3.29.0'


def check_commitizen_version():
    print('CHECK CHECK Checking Commitizen version...')
    try:
        # Find the full path of the cz executable
        cz_path = shutil.which('cz')
        if cz_path is None:
            raise FileNotFoundError('Commitizen (cz) not found in PATH')

        # Check the installed version of Commitizen
        output = subprocess.check_output([cz_path, 'version'], text=True)  # noqa: S603
        version = output.strip().split()[-1]
        if version < MINIMUM_COMMITIZEN_VERSION:
            raise SystemExit(
                f'Error: Found an older version of Commitizen installed globally (v{version}). '
                f'Please uninstall it or use a virtual environment with Commitizen >= {MINIMUM_COMMITIZEN_VERSION}.'
            )
    except FileNotFoundError:
        # Commitizen is not installed globally, proceed
        pass
    except Exception as error:  # pylint: disable=broad-except
        sys.exit(f'Unexpected error while checking Commitizen version: {error}')


# Run the version check before installation
check_commitizen_version()
