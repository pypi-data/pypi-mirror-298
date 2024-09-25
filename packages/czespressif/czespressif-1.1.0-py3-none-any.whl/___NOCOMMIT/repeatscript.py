# pylint: disable=W
import os
import subprocess
import sys


# Capture the original command that triggered the pre-commit hook
def get_original_command():
    try:
        # Fetch the parent process command (the original command that triggered the pre-commit)
        original_command = subprocess.check_output(['ps', '-ocommand=', '-p', str(os.getppid())]).decode('utf-8').strip()
        return original_command
    except Exception as e:
        print(f'Error capturing the original command: {e}')
        sys.exit(1)


# Update the changelog using commitizen
def update_changelog():
    try:
        subprocess.run('cz changelog > /dev/null', shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f'Error updating the changelog: {e}')
        sys.exit(1)


# Check if CHANGELOG.md was modified
def is_changelog_modified():
    try:
        modified_files = subprocess.check_output(['git', 'diff', '--name-only']).decode('utf-8').splitlines()
        return 'CHANGELOG.md' in modified_files
    except subprocess.CalledProcessError as e:
        print(f'Error checking modified files: {e}')
        sys.exit(1)


# Stage the changelog if modified
def stage_changelog():
    try:
        subprocess.run(['git', 'add', 'CHANGELOG.md'], check=True)
    except subprocess.CalledProcessError as e:
        print(f'Error staging CHANGELOG.md: {e}')
        sys.exit(1)


# Re-run the original command
def rerun_original_command(original_command):
    try:
        print(f'Re-running the original command: {original_command}')
        subprocess.run(original_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f'Error re-running the original command: {e}')
        sys.exit(1)


def main():
    print('Running repeat script')
    # Capture the original command
    original_command = get_original_command()

    # Update the changelog
    update_changelog()

    # Check if CHANGELOG.md was modified
    if is_changelog_modified():
        print('CHANGELOG.md modified. Staging the file...')
        # Stage the modified changelog
        stage_changelog()

        # Re-run the original command to trigger pre-commit again
        rerun_original_command(original_command)
    else:
        print('No changes to CHANGELOG.md, proceeding with the original command.')


if __name__ == '__main__':
    main()
