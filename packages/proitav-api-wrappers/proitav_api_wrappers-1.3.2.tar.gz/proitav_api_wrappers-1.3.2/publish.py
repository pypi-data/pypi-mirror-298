import subprocess
import sys
import re


def get_current_version():
    with open("setup.py", "r") as f:
        content = f.read()
        match = re.search(r'version="(\d+\.\d+\.\d+)"', content)
        if match:
            return match.group(1)
    raise ValueError("Version not found in setup.py")


def update_version(current_version, release_type):
    major, minor, patch = map(int, current_version.split("."))
    if release_type == "major":
        return f"{major + 1}.0.0"
    elif release_type == "minor":
        return f"{major}.{minor + 1}.0"
    elif release_type == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError("Invalid release type. Use 'major', 'minor', or 'patch'.")


def update_setup_py(new_version):
    with open("setup.py", "r") as f:
        content = f.read()

    updated_content = re.sub(
        r'version="(\d+\.\d+\.\d+)"', f'version="{new_version}"', content
    )

    with open("setup.py", "w") as f:
        f.write(updated_content)


def run_command(command):
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    output, error = process.communicate()
    if process.returncode != 0:
        print(f"Error executing command: {command}")
        print(error.decode())
        sys.exit(1)
    return output.decode().strip()


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ["major", "minor", "patch"]:
        print("Usage: python publish.py [major|minor|patch]")
        sys.exit(1)

    release_type = sys.argv[1]
    current_version = get_current_version()
    new_version = update_version(current_version, release_type)

    print(f"Updating version from {current_version} to {new_version}")
    update_setup_py(new_version)

    run_command("git add setup.py")
    run_command(f'git commit -m "Bump version to {new_version}"')
    run_command("git push origin main")

    run_command(f'git tag -a v{new_version} -m "Release version {new_version}"')
    run_command(f"git push origin v{new_version}")

    print(f"Version {new_version} has been released!")


if __name__ == "__main__":
    main()
