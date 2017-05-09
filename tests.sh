#!/bin/bash

pushd script.MyOSMC/resources/lib

# Run pylint
pylint .

# Run unit tests

pytest
