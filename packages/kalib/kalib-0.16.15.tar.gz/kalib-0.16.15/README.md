# Tasks

## ver

requires: env

Deploys a new tag for the repo.

```bash

#

# uncommited="$(git diff --cached --name-only | sort -u | tr '\n' ' ' | xargs)"
# if [ -n "$uncommited" ]; then
#     echo "uncommited changes found"
#     exit 1
# fi

#

branch="$(git rev-parse --quiet --abbrev-ref HEAD 2>/dev/null)"
if [ -z "$branch" ]; then
    exit 1
elif [ "$branch" == "master" ]; then
    echo "using main master mode"
else
    exit 1
fi

#

changes="$(git ls-files --deleted --modified --exclude-standard)"
changes="$(printf "$changes" | sort -u | tr '\n' ' ' | xargs)"

if [ "$changes" == "README.md" ]; then
    echo "pipeline development mode"
elif [ -n "$changes" ]; then
    echo "uncommited changes found"
    exit 1
fi

current="$(git describe --tags --abbrev=0)"
[ -z "$current" ] && exit 1


amount="$(git rev-list --count $current..HEAD)"
uncommited="$(git diff --cached --name-only | sort -u | tr '\n' ' ' | xargs)"

if [ "$amount" -eq 0 ] && [ -z "$uncommited" ]; then
    echo "no changes since $current"
    exit 1
fi

version="$(bump patch "$current")"
[ -z "$version" ] && exit 1

#

xc set "$current" "$version"

uncommited="$(git diff --cached --name-only | sort -u | tr '\n' ' ' | xargs)"
changes="$(git ls-files --deleted --modified --exclude-standard)"
changes="$(printf "$changes" | sort -u | tr '\n' ' ' | xargs)"

if [[ "$uncommited" =~ "\bpyproject\.toml\b" ]] || [[ "$changes" =~ "\bpyproject\.toml\b" ]]; then
    xc commit-project
fi

if [[ "$uncommited" =~ "\bci/\.pre-commit-config\.yaml\b" ]] || [[ "$changes" =~ "\bci/\.pre-commit-config\.yaml\b" ]]; then
    xc commit-config
fi

uncommited="$(git diff --cached --name-only | sort -u | tr '\n' ' ' | xargs)"
if [ -n "$uncommited" ]; then
    git commit -m "$branch: $version"
fi

git tag -a "$version" -m "$version" && \
git push --tags && \
git fetch --tags --force

echo "version update to ${version}"
```

## set

run: once
requires: env, commit-update

Update version in pyproject.toml.

```python
#!.env/bin/python
from os import environ
from sys import argv, exit
from re import match
from pathlib import Path

import tomli_w
import tomllib

ROOT = Path(environ['PWD'])

def get_version(string):
    try:
        return match(r'^(\d+\.\d+\.\d+)$', string).group(1)
    except Exception:
        print(f'could not parse version from {string}')
        exit(3)

if __name__ == '__main__':
    try:
        current_tag = get_version(argv[1])
        version_tag = get_version(argv[2])
    except IndexError:
        print('usage: xc setver <old_tag> <new_tag>')
        exit(1)

    path = ROOT / 'pyproject.toml'
    try:
        with open(path, 'rb') as fd:
            data = tomllib.load(fd)

    except Exception:
        print(f'could not load {path}')
        exit(2)

    try:
        current_ver = get_version(data['tool']['poetry']['version'])
        print(f'project version: {current_ver}')

    except KeyError:
        print(f'could not find version in {data}')
        exit(2)

    if current_tag != current_ver:
        if current_ver == version_tag:
            print(f'current version {current_ver} == {version_tag}, no update needed')
            exit(0)

        print(f'current tag {current_tag} != {current_ver} current version')
        exit(4)

    data['tool']['poetry']['version'] = version_tag
    try:
        with open(path, 'wb') as fd:
            tomli_w.dump(data, fd)

        print(f'project version -> {version_tag}')

    except Exception:
        print(f'could not write {path} with {data=}')
        exit(5)
```

## new

requires: env, ver

Publishes a new version to pypi.

```bash
.env/bin/poetry build
.env/bin/poetry publish

```

## env

run: once

Creates a virtualenv for the project.

```bash

if [ ! -d ".env" ]; then
    virtualenv --python python3.11 ".env" && \
    source ".env/bin/activate" && \
    .env/bin/pip install --upgrade pip && \
    .env/bin/pip install --upgrade poetry pre-commit tomli_w

else
    [ -f ".env/bin/activate" ]

fi
```

## pre

requires: env, commit-update

Runs pre-commit checks.

```bash
.env/bin/pre-commit run --config ci/.pre-commit-config.yaml --all
```

## commit-config

requires: env, commit-update

Runs pre-commit checks.

```bash

.env/bin/pre-commit run check-yaml --config ci/.pre-commit-config.yaml --color always --file ci/.pre-commit-config.yaml || value="$?"

while true; do
    value="0"
    .env/bin/pre-commit run yamlfix --config ci/.pre-commit-config.yaml --color always --file ci/.pre-commit-config.yaml || value="$?"

    if [ "$value" -eq 0 ]; then
        break

    elif [ "$value" -eq 1 ]; then
        continue

    else
        exit "$value"

    fi
done

changes="$(git diff pyproject.toml)" || exit "$?"
changes="$(printf "$changes" | wc -l)"
if [ "$changes" -ne 0 ]; then
    git add ci/.pre-commit-config.yaml
fi

```

## commit-project

requires: env, commit-update

Format and commit: pyproject.toml

```bash

.env/bin/pre-commit run check-toml --config ci/.pre-commit-config.yaml --color always --file pyproject.toml || value="$?"

while true; do
    value="0"
    .env/bin/pre-commit run pretty-format-toml --config ci/.pre-commit-config.yaml --color always --file pyproject.toml || value="$?"

    if [ "$value" -eq 0 ]; then
        break

    elif [ "$value" -eq 1 ]; then
        continue

    else
        exit "$value"

    fi
done

changes="$(git diff pyproject.toml)" || exit "$?"
changes="$(printf "$changes" | wc -l)"
if [ "$changes" -ne 0 ]; then
    git add pyproject.toml
fi

```

## commit-update

run: once
requires: env

pre-commit update when needed

```bash

ctime="$(date +%s)"
mtime="$(git log -1 --format=%ct ci/.pre-commit-config.yaml)"

result=$(((7*86400) - (ctime - mtime)))

if [ "$result" -le 0 ]; then
    .env/bin/pre-commit autoupdate --config ci/.pre-commit-config.yaml
fi

```
