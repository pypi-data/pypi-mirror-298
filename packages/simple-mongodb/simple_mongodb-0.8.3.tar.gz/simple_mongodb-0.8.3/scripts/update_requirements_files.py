from typing import Any

import toml


def update_requirements_file(requirements_file: str, dependencies: list[str]) -> None:
    with open(file=requirements_file, mode='w') as file:
        for dependencie in dependencies:
            file.write(dependencie)
            file.write('\n')


def get_dependencies(pyproject_content: dict[str, Any], dev: bool = False) -> list[str]:
    project: str | None = pyproject_content.get('project')

    if not project:
        raise ValueError('project not found in pyproject.toml')

    if not dev:
        dependencies: list[str] | None = project.get('dependencies')
        if not isinstance(dependencies, list):
            raise ValueError('dependencies not found in pyproject.toml')
        return dependencies

    optional_dependencies: dict[str, list[str]] | None = project.get(
        'optional-dependencies'
    )
    if not isinstance(optional_dependencies, dict):
        raise ValueError('optional-dependencies not found in pyproject.toml')

    dependencies: list[str] | None = optional_dependencies.get('dev')
    if not isinstance(dependencies, list):
        raise ValueError('dev dependencies not found in pyproject.toml')

    return dependencies


def main() -> None:
    pyproject_content: dict[str, Any] = toml.load('pyproject.toml')

    update_requirements_file(
        requirements_file='requirements.txt',
        dependencies=get_dependencies(pyproject_content=pyproject_content),
    )

    update_requirements_file(
        requirements_file='requirements-dev.txt',
        dependencies=get_dependencies(pyproject_content=pyproject_content, dev=True),
    )


if __name__ == '__main__':
    main()
