#!/bin/bash

TARGETDIR=/tmp/strats

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
  echo -n "${basename}: "
  THISTARGETDIR=$TARGETDIR/${basename%%.svg}
  mkdir $THISTARGETDIR
  cp "$file" $THISTARGETDIR/ORIG.svg
  for strat in KEEP AGGREGATE DECOMPOSE_MATRIX DECOMPOSE_MATRIX_AND_AGGREGATE CANONICAL_CONSERVATIVE CANONICAL_AGGRESSIVE
  do
    targetname=$THISTARGETDIR/${strat}.svg
    ./run_rewrite.sh --transform-strategy $strat < $file > $targetname
  done
done

)



