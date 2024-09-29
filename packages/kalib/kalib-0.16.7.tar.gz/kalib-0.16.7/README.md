https://xcfile.dev/task-syntax/scripts/

# Tasks
## ver

Deploys a new tag for the repo.

```zsh

branch="$(git rev-parse --quiet --abbrev-ref HEAD 2>/dev/null)"

#
if [ -z "$branch" ]; then
    exit 1
elif [ "$branch" == "master" ]; then
    echo "using main master mode"
else
    exit 1
fi

#

changes="$(git ls-files --deleted --modified --exclude-standard /my/src/lib/kalib)"
changes="$(printf "$changes" | sort -u | tr '\n' ' ' | xargs)"

if [ "$changes" == "README.md" ] || [ "$changes" == "pyproject.toml README.md" ]; then
    echo "pipeline development mode"
elif [ -n "$changes" ]; then
    exit 1
fi

current="$(git describe --tags --abbrev=0)"
[ -z "$current" ] && exit 1


amount="$(git rev-list --count $current..HEAD)"
if [ "$amount" -eq 0 ]; then
    echo "no changes since $current"
    exit 1
fi

version="$(bump patch "$current")"
[ -z "$version" ] && exit 1

xc set "$current" "$version"

while true; do
    value="0"
    pre-commit run --config ci/.pre-commit-config.yaml --color always --file pyproject.toml || value="$?"

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
    git add pyproject.toml && \
    git commit -m "$branch: $version"
fi

git tag -a "$version" -m "$version" && \
git push --tags && \
git fetch --tags --force

echo "version update to ${version}"
```

## set

Update version in pyproject.toml.

```python
#!/usr/bin/env python3.11
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

Publishes a new version to pypi.

```zsh
xc ver
poetry build && poetry publish
```
