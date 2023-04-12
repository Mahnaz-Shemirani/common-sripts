#!/bin/bash -l
set -eu

# define variables
proj=u2021014
email=mahnaz.irani-shemirani@umu.se
in=$(realpath ../PATH to DATA)
out=$(realpath ../PATH to OUT)
singularity=$(realpath ../Path to singularity.sif)
ref_fasta=$(realpath ../reference/PATH TO FASTA.fa)
inx_dir=$(realpath ../reference/PATH to indices)


if [ ! -d $out ]; then
  mkdir -p $out
fi

# env
export SINGULARITY_BINDPATH="/mnt:/mnt"

# run
for fq in $(find $in -name "*_1.fq.gz"); do

sbatch -A $proj --mail-user $email	runSortmerna.sh  $singularity $out $ref_fasta $inx_dir $fq ${fq/_1.fq.gz/_2.fq.gz}
	
done

