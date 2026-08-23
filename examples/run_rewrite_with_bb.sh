#!/bin/bash

( 
cd $(dirname $0)
PYTHONPATH=../src python3 rewrite_with_bb.py $*
)

