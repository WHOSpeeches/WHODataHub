# The WHO's Director General's Speeches

![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![MIT license](https://img.shields.io/badge/License-MIT-green.svg)
![Last Updated](https://img.shields.io/badge/Last%20Updated-2023.01.26-success.svg)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4391412.svg)](https://doi.org/10.5281/zenodo.4391412)

Below is the Gen 2 service for retrieving the WHO's Director General's Speeches.

# Operation

## Install

You can install the package using the following steps:

`pip` install using an _admin_ prompt.

```{ps1}
pip uninstall WHOSpeeches
python -OO -m pip install -v git+https://github.com/WHOSpeeches/data.git
```

or if you have the code local

```{ps1}
pip uninstall WHOSpeeches
python -OO -m pip install -v c:/repos/WHOSpeeches/data
```

## Run

Get all the WHO's Director General's Speeches.

```{ps1}
WHOSpeeches -dest "c:/data/who"
```

The following are required parameters:

* `dest` is the location of the retrieved speeches.

## Debug

The code in this repo is setup as a module.
[Debugging](https://code.visualstudio.com/docs/python/debugging#_module) is based on the assumption that the module is already installed.
In order to debug (F5), make sure to install the module as editable (see below).

```{ps1}
pip uninstall WHOSpeeches
python -m pip install -e c:/repos/WHOSpeeches/data
```

When debugging in VSCode for the first time, consider adding the below config to the _launch.json_ file.

```{json}
"args" : ["-dest", "d:/data/who"]
```
