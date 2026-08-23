#!/bin/bash

SVG_TEST_DEST_DIR=/tmp/svg

CONFFILE="$(dirname $0)/all.conf"
if [[ -r $CONFFILE ]]
then
  . $CONFFILE
fi


TARGETDIR=${SVG_TEST_DEST_DIR}/path_options

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
  echo -n "${basename}: "
  THISTARGETDIR=$TARGETDIR/${basename%%.svg}
  mkdir $THISTARGETDIR
  cp "$file" $THISTARGETDIR/ORIG.svg

  for coord in ABSOLUTE RELATIVE KEEP
  do
    for compact in CANONICAL COMPACT
    do
      for commandset in BASE FULL
      do
        targetname=$THISTARGETDIR/${coord}_${compact}_${commandset}.svg
        ./run_rewrite.sh --path-coordinates ${coord} --path-compactness ${compact} --path-command-set ${commandset} \
		         < $file > $targetname
	echo "$targetname"
      done
    done
  done
done
)



