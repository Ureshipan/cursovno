#!/bin/bash

cd $(dirname $0)/model

# pisoFoam
foamRun -solver incompressibleFluid
