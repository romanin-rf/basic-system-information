@echo off
python -m pip uninstall bsipack
python setup.py bdist_wheel
python -m pip install dist\bsipack-0.3.1-py3-none-any.whl