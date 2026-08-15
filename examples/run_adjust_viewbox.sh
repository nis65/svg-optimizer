#!/bin/bash

( 
cd $(dirname $0)
PYTHONPATH=../src python3 adjust_viewbox.py $*
)
