@ECHO OFF

pushd %~dp0

python3 setup.py bdist_wheel
twine upload dist/*
