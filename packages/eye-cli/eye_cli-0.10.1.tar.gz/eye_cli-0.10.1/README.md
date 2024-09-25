# eye

The CLI for moving files and processing photogrammetry data. 

## Install

```
pipx install eye-cli
```

open a new terminal

```
eye --install-completion
```


## Upgrade

```
pipx upgrade eye-cli
```

## Publish

First bump the version number in `pyproject.toml`.
Then:

```
➜ poetry publish --build

There are 1 files ready for publishing. Build anyway? (yes/no) [no] yes
Building eye-cli (0.1.0)
  - Building sdist
  - Built eye_cli-0.1.0.tar.gz
  - Building wheel
  - Built eye_cli-0.1.0-py3-none-any.whl

Publishing eye-cli (0.1.0) to PyPI
 - Uploading eye_cli-0.1.0-py3-none-any.whl 100%
 - Uploading eye_cli-0.1.0.tar.gz 100%
```

