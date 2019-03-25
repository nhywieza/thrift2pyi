#! /usr/bin/env bash
set -e

flake8 --exclude venv/,.eggs,.tox
