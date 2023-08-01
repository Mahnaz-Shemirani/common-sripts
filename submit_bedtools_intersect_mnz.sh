#!/bin/bash -l

set -eu

# define variables
proj=u2021014
email=mahnaz.irani-shemirani@umu.se
fileA=$(realpath ../results/Lalbus.bed)
dirB=$(realpath ../results/dirB)
out=$(realpath ../results/bedtool)
singularity=$(realpath ../singularity/bedtools_2.30.0.sif)

if [ ! -d $out ]; then
  mkdir -p $out
fi

# env
export SINGULARITY_BINDPATH="/mnt:/mnt"

sbatch -w franklin -A $proj --mail-user $email runBedToolsIntersect.sh 
$singularity $fileA $dirB $out




