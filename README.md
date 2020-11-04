# Gameta

Gameta is a powerful CLI tool that helps you to manage [meta-repositories] 
or [metarepos]. It allows you to creates links to related repositories, 
make changes and sync them, and provides functionality to customise and 
apply other CLI commands to these repositories.

Gameta is a play on the word gamete (reproductive cells), and similar 
to how gametes form the building blocks for life, gameta helps to 
manage the many repositories that form the building blocks for more
complex software.

## System Requirements

Gameta requries Python 3.7+, it is designed to be multi-platform but currently
only tested in Linux environments.

## Installation

Gameta can be easily installed and updated via pip:

```bash
$ pip install gameta  # install
$ pip install -U gameta  # update
```

## Getting Started

Getting started is really easy.

```bash
gameta init
gameta init -g  # To initialise directory as a Git repo 
```

Gameta will extract git information and create the .meta file which stores 
all your project configurations.

```json
{
  "projects": {
    "gameta": {
      "path": ".",
      "tags": ["metarepo"],
      "url": "https://github.com:genius-systems/gameta.git"
    }
  }
}
```

___
**Note**

If your project has not been initialised with Git, you can specify the
`--git` or `-g` flag to perform a git init, but you will have to update the
repository URL manually later on. 
___

If your repository contains a .meta file generated by Gameta, simply run the
following command to sync all linked repositories locally:

```bash
gameta sync
```

## Adding a Repository

Run the following command to add a new repository.

```bash
gameta repo add -n GitPython -u https://github.com/gitpython-developers/GitPython.git -p GitPython
```

___
**Note**

The path variable is the relative path within the metarepo itself
___

You should see another entry under the projects object within the .meta file

```json
{
  "projects": {
    "gameta": {
      "path": ".",
      "tags": ["metarepo"],
      "url": "git@github.com:genius-systems/gameta.git"
    },
    "GitPython": {
      "path": "GitPython",
      "tags": ["a", "b", "c"],
      "url": "https://github.com/gitpython-developers/GitPython.git"
    }
  }
}
```

You should also see the repository cloned to the relative path specified

## Applying commands

Gameta provides a powerful toolkit to manage your set of repositories.

```bash
gameta apply -c "git fetch --all --tags --prune" -c "git merge"
```

The command above applies the following to all repositories:

1. Fetches all git updates, tags and prunes redundant git artifacts
2. Merges changes on the default branch

## Documentation 

Documentation can be found at [Gameta Docs]

[Gameta Docs]: https://genius-systems.github.io/gameta