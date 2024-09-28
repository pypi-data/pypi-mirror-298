import os
import requests
import subprocess


def has_code(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line and not stripped_line.startswith('#'):
                return True
    return False

def find_non_empty_init_files(directory):
    init_files_with_code = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file == '__init__.py':
                file_path = os.path.join(root, file)
                if has_code(file_path):
                    init_files_with_code.append(file_path)

    return init_files_with_code

def find_large_python_files(directory, min_lines=300):
    large_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    num_lines = sum(1 for _ in f)
                    if num_lines > min_lines:
                        large_files.append((file_path, num_lines))

    return large_files

def line_length_counter(directory):
    report = {
        'less_than_80': 0,
        'between_80_and_99': 0,
        'between_100_and_119': 0,
        'more_than_120': 0,
    }
    for root, _, files in os.walk(directory):
        for file in files:
            if not file.endswith('.py'):
                continue
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line_length = len(line)
                    if line_length < 80:
                        report['less_than_80'] += 1
                    elif 80 <= line_length <= 99:
                        report['between_80_and_99'] += 1
                    elif 100 <= line_length <= 119:
                        report['between_100_and_119'] += 1
                    else:
                        report['more_than_120'] += 1
    return report


def get_latest_version(package_name):
    url = f'https://pypi.org/pypi/{package_name}/json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['info']['version']
    else:
        return None


def get_dependencies_versions():
    # read the versions of the dependencies via pip
    # and compare them with the last version available on pypi
    result = subprocess.run(['pip', 'freeze'], stdout=subprocess.PIPE, text=True)

    packages = {}
    for line in result.stdout.split('\n'):
        if '==' in line:
            package, version = line.split('==')
            packages[package] = {'installed_version': version}

    for package, versions in packages.items():
        latest_version = get_latest_version(package)
        if latest_version:
            versions['latest_version'] = latest_version

    return packages


def get_dependencies_version_diffs():
    """
    using semver, we want to return the list of packages that have a minor or major difference

    minor: 1.0.0 -> 1.1.0
    major: 1.0.0 -> 2.0.0

    We ignore the patch version because, hey, it's ok
    """
    diffs = {
        'minor': [],
        'major': []
    }

    packages = get_dependencies_versions()
    for package, versions in packages.items():
        installed_version = versions['installed_version']
        latest_version = versions.get('latest_version')
        if not latest_version:
            continue
        if installed_version == latest_version:
            continue
        installed_major, installed_minor, _ = installed_version.split('.')
        latest_major, latest_minor, _ = latest_version.split('.')
        if installed_major != latest_major:
            diffs['major'].append((package, installed_version, latest_version))
        elif installed_minor != latest_minor:
            diffs['minor'].append((package, installed_version, latest_version))
    return diffs
