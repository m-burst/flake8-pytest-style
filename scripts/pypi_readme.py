#!/usr/bin/env python3
import pathlib
import re
from typing import Match, cast

import tomlkit
from tomlkit.container import Container


def process_readme(readme: str, project_metadata: Container) -> str:
    repository = cast(str, project_metadata['repository'])
    version = cast(str, project_metadata['version'])
    base_url = f'{repository}/blob/v{version}/'

    def replace_url(match: Match[str]) -> str:
        path_without_leading_slash = match.group(0).lstrip('/')
        return f'{base_url}{path_without_leading_slash}'

    return re.sub(r'/?\S+\.md', replace_url, readme)


def make_output_filename(input_filename: str) -> str:
    path = pathlib.Path(input_filename)
    return str(path.parent / f'{path.stem}-pypi{path.suffix}')


def main() -> None:
    with open('pyproject.toml') as pyproject_file:
        pyproject_data = tomlkit.loads(pyproject_file.read())
    project_metadata = cast(
        Container, cast(Container, pyproject_data['tool'])['poetry']
    )

    readme_filename = cast(str, project_metadata['readme'])
    with open(readme_filename) as input_file:
        input_readme = input_file.read()

    output_readme = process_readme(input_readme, project_metadata)
    output_filename = make_output_filename(readme_filename)
    with open(output_filename, 'w') as output_file:
        output_file.write(output_readme)

    project_metadata['readme'] = output_filename
    with open('pyproject.toml', 'w') as pyproject_file:
        pyproject_file.write(tomlkit.dumps(pyproject_data))


if __name__ == '__main__':
    main()
