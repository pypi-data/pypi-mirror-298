import os


class MissingCangelogForVersion(Exception):
    pass


def get_package_version() -> str:
    return os.getenv('PACKAGE_VERSION', '0.0.0')


def main() -> None:
    version: str = get_package_version()

    print(f'PACKAGE_VERSION: {version}')

    with open(file='CHANGELOG.md', mode='r') as file:
        content: str = file.read()

        if f'### Version - {version} (' not in content:
            raise MissingCangelogForVersion(f'Changelog for {version} is not found')


if __name__ == '__main__':
    main()
