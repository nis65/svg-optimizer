#!/bin/bash

SVG_TEST_DEST_DIR=/tmp/svg

CONFFILE="$(dirname $0)/all.conf"
if [[ -r $CONFFILE ]]
then
  . $CONFFILE
fi

TARGETDIR=${SVG_TEST_DEST_DIR}/boundingboxed
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
  echo "===== bounding box for $file"
  basename=$( basename $file )
  ./run_getbbox.sh < $file

  THISTARGETFILE="${basename%%.svg}_bounding_box_drawed.svg"
  target=${TARGETDIR}/$THISTARGETFILE
  ./run_rewrite_with_bb.sh < $file > $target

  THISTARGETFILE="${basename%%.svg}_viewbox_adjusted.svg"
  target=${TARGETDIR}/$THISTARGETFILE
  ./run_adjust_viewbox.sh < $file > $target
done

)
