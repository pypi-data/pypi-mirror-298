import os

import toml


class VersionNotSameError(Exception):
    pass


def get_version_from_init_file() -> str:
    with open(file='simple_mongodb/__init__.py', mode='r') as file:
        for line in file.readlines():
            if not '__version__ = ' in line:
                continue
            return line.replace('__version__ = ', '').replace('\'', '')[0:-1]


def get_version_from_pyproject_toml() -> str:
    file: str = 'pyproject.toml'
    if not os.path.isfile(file):
        raise FileNotFoundError(f'{file} no found')

    data: dict[str, Any] = toml.load(file)

    project: dict[str, Any] | None = data.get('project', None)
    if not project:
        raise ValueError(f'project is not found in {file}')

    version: str | None = project.get('version', None)
    if not version:
        raise ValueError(f'version is not found in {file}')

    return version


def main() -> None:
    init_file_version: str = get_version_from_init_file()
    pyproject_version: str = get_version_from_pyproject_toml()

    print(f'init-file-version: {init_file_version}')
    print(f'pyproject.toml-version: {pyproject_version}')

    if not init_file_version == pyproject_version:
        raise VersionNotSameError('The versions are not the same')

    if os.getenv('GITHUB_ACTIONS') == 'true':
        os.system(f'echo "PACKAGE_VERSION={pyproject_version}" >> $GITHUB_ENV')


if __name__ == '__main__':
    main()
