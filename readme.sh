#!/bin/bash
jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace *.ipynb
jupyter nbconvert --ClearOutputPreprocessor.enabled=True --to markdown --output readme.md readme.ipynb
