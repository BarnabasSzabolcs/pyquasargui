#!/usr/bin/env bash
# Creates a dist and uploads it to pip
python -m build
python3 -m twine upload dist/*