# conda_rocker

## Continuous Integration Status

[![Ci](https://github.com/blooop/conda_rocker/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/blooop/conda_rocker/actions/workflows/ci.yml?query=branch%3Amain)
[![Codecov](https://codecov.io/gh/blooop/conda_rocker/branch/main/graph/badge.svg?token=Y212GW1PG6)](https://codecov.io/gh/blooop/conda_rocker)
[![GitHub issues](https://img.shields.io/github/issues/blooop/conda_rocker.svg)](https://GitHub.com/blooop/conda_rocker/issues/)
[![GitHub pull-requests merged](https://badgen.net/github/merged-prs/blooop/conda_rocker)](https://github.com/blooop/conda_rocker/pulls?q=is%3Amerged)
[![GitHub release](https://img.shields.io/github/release/blooop/conda_rocker.svg)](https://GitHub.com/blooop/conda_rocker/releases/)
[![License](https://img.shields.io/github/license/blooop/conda_rocker)](https://opensource.org/license/mit/)
[![Python](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/downloads/)
[![Pixi Badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/prefix-dev/pixi/main/assets/badge/v0.json)](https://pixi.sh)

## Intro

This is a [rocker](https://github.com/tfoote/rocker) extension for adding [conda](https://github.com/conda/conda) to an existing docker image.  Check out the [rocker](https://github.com/osrf/rocker) GitHub page for more details on how Rocker and its extensions work. In short, Rocker allows you to add custom capabilities to existing Docker containers.

The installer uses [miniforge](https://github.com/conda-forge/miniforge) instead of conda as it's a lightweight and [free](https://stackoverflow.com/questions/60532678/what-is-the-difference-between-miniconda-and-miniforge). 


## Installation

```
pip install conda-rocker
```

## Usage

To install conda in an image use the `--conda` flag

```
#add conda to the ubuntu:22.04 image
rocker --conda ubuntu:22.04

# add conda to the nvidia/cuda image
rocker --conda nvidia/cuda
```
