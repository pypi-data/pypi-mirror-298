import os


def install_dependencies(requirements_file: str) -> None:
    if not os.path.isfile(requirements_file):
        raise FileNotFoundError(f'{requirements_file} no found')
    os.system(f'pip install -r {requirements_file}')


def main() -> None:
    install_dependencies(requirements_file='requirements.txt')
    install_dependencies(requirements_file='requirements-dev.txt')


if __name__ == '__main__':
    main()
