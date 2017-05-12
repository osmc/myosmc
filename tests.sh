#!/bin/bash

# pushd script.MyOSMC/resources/lib

# Run pylint
pylint $(pwd)

# Run unit tests

pytest
