#!/usr/bin/env bash

while getopts i:o: OPT; do
  case $OPT in
  "i") imagesdir=$OPTARG ;;
  "o") outputdir=$OPTARG ;;
  *) exit 1 ;;
  esac
done

if [ ! -v imagesdir ]; then
  exit 1
fi

if [ ! -v outputdir ]; then
  exit 1
fi

workdir=$(
  cd "$(dirname "$0")" || exit
  pwd
)

docker build -t manga-line-extraction:cpu "$workdir"

# titles=$(ls "$imagesdir")
titles=$(ls "$imagesdir" | fzf -m --reverse)

for title in $titles; do
  echo "$title"
  inputidr="$imagesdir/$title"

  mkdir -p "$outputdir/$(basename "$inputidr")"
  docker run \
    --rm \
    -v "$workdir":/work/app \
    -v "$inputidr":/work/input:ro \
    -v "$outputdir/$(basename "$inputidr")":/work/output \
    manga-line-extraction:cpu \
    python test_mse.py /work/input /work/output
done
