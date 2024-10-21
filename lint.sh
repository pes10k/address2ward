#!/bin/bash

pylint address2ward *.py
mypy --strict .
