#!/bin/bash

#SBATCH --job-name=test
#SBATCH --gres=gpu:0
#SBATCH --mem-per-cpu=2048
#SBATCH --time=4-00:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=shivprasad.sagare@research.iiit.ac.in

source activate wikidata_handler
BASE_DIR=/scratch/shivprasad.sagare

if [ -d "$BASE_DIR" ]; then
    rm -rf $BASE_DIR
fi

mkdir -p $BASE_DIR

scp shivprasad.sagare@ada:/share1/shivprasad.sagare/wikimapper/data/index_hiwiki-latest.db $BASE_DIR

cd /home2/shivprasad.sagare/indic_wikibot/wikidata/wikimapper/
echo "Current directory ${PWD}"

python code.py

scp $BASE_DIR/output.json shivprasad.sagare@ada:/share1/shivprasad.sagare/wikimapper

rm -rf /scratch/shivprasad.sagare