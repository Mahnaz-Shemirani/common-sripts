#!/bin/bash -l
#SBATCH -p core
#SBATCH -n 1
#SBATCH -t 2:00:00
#SBATCH --mail-type=ALL
## -A and --mail-user set in the submit job

## stop on error
set -ex

## we get one dir and one file as input
export USAGETXT="Usage: $0 <singularity container> <a file> <dirB> <out dir> [bed intersect option]"

# load functions
source ${SLURM_SUBMIT_DIR:-$(pwd)}/../UPSCb-common/src/bash/functions.sh

# test the param
# checks
[[ $# != 4 ]] && abort "This function expects 5 arguments"

[[ ! -f $1 ]] && abort "The first argument needs to be the bedtools singularity container file"

## enforce singularity
[[ -z ${SINGULARITY_BINDPATH:-} ]] && abort "This function relies on singularity, set the SINGULARITY_BINDPATH environment variable"

[[ ! -f $2 ]] && abort "The second argument needs to be an existing file"

[[ ! -d $3 ]] && abort "The third argument needs to be an existing directory of files"

[[ ! -d $4 ]] && abort "The fifth argument needs to be an existing directory"


# Loop over all b files in the directory
for fileB in "$dirB"/*.bed; do
# Define the output file name based on the input file names
outfile="$4/$(basename $2_$(basename $3)_overlap.bed"

## get the intersct results
singularity exec $1 bedtools intersect -a $2 -b $fileB > $outfile
