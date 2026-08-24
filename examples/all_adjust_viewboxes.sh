#!/bin/bash

SVG_TEST_DEST_DIR=/tmp/svg

CONFFILE="$(dirname $0)/all.conf"
if [[ -r $CONFFILE ]]
then
  . $CONFFILE
fi

TARGETDIR=${SVG_TEST_DEST_DIR}/viewboxed
if [[ -r $TARGETDIR && -w $TARGETDIR && -d $TARGETDIR ]]
then
  true
else
  mkdir -p $TARGETDIR
fi
rm -rf $TARGETDIR/*

echo "Results in $TARGETDIR"

(
cd $(dirname $0)

for file in ../tests/testdata/*svg
do
  basename=$( basename $file )
  THISTARGETFILE="${basename%%.svg}_adjusted_viewbox.svg"
  target=${TARGETDIR}/$THISTARGETFILE
  echo "creating $target"
  ./run_adjust_viewbox.sh < $file > $target
done

)
