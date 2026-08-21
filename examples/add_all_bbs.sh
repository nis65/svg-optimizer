#!/bin/bash

TARGETDIR=/tmp/boundingboxed
if [[ -r $TARGETDIR && -w $TARGETDIR && -d $TARGETDIR ]]
then
  true
else
  mkdir $TARGETDIR
fi
rm -rf $TARGETDIR/*

echo "Results in $TARGETDIR"

(
cd $(dirname $0)

for file in ../tests/testdata/*svg
do
  basename=$( basename $file )
  THISTARGETFILE="${basename%%.svg}_with_bb.svg"
  target=${TARGETDIR}/$THISTARGETFILE
  echo "creating $target"
  ./run_rewrite_with_bb.sh < $file > $target
done

)




