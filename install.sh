#! /usr/bin/env bash

echo "Uninstalling..." &&
pip uninstall acd -y > /dev/null &&
echo "Building..." &&
rm ./dist -rf &&
python3 -m build > /dev/null &&
echo "Installing..." &&
pip install dist/acd*.whl > /dev/null
