#!/bin/bash -l
#SBATCH -p core
#SBATCH -n 10
#SBATCH -t 48:00:00
#SBATCH --mail-user=aman.zare@umu.se
#SBATCH --mail-type=END

# fail on ERROR
set -eux

# load helpers
source ${SLURM_SUBMIT_DIR:-$(pwd)}/../UPSCb-common/src/bash/functions.sh

# usage
USAGETXT=\
"
 $0 <singularity image> <input> <output>
"

## arguments
[[ $# -ne 3 ]] && abort "This script takes three arguments"
[[ ! -f $1 ]] && abort "The first argument needs to be an existing singularity seqtk container file"
[[ ! -f $2 ]] && abort "The second argument needs to be an existing fastq file"
[[ ! -f $3 ]] && abort "The third argument needs to be fastq file "


## enforce singularity
[[ -z ${SINGULARITY_BINDPATH:-} ]] && abort "This function relies on singularity, set the SINGULARITY_BINDPATH environment variable"

## start
singularity exec $1 trimfq -b 4 -e 4 $2 > $3

