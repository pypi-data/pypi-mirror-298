#! /bin/bash
#$ -j y # Merge the error and output streams into a single file
#$ -o /unix/cedar/egan/rebuild_contur_ref_area/myscan00/13TeV/0009/contur.log # Output file path
source /unix/cedar/software/cos7/Herwig-repo_Rivet-repo/setupEnv.sh;
export CONTUR_DATA_PATH=/home/egan/contur
export CONTUR_USER_DIR=/home/egan/contur_users
export RIVET_ANALYSIS_PATH=/home/egan/contur/contur_user:/home/egan/contur/data/Rivet
export RIVET_DATA_PATH=/home/egan/contur/contur_user:/home/egan/contur/data/Rivet:/home/egan/contur/data/Theory
source $CONTUR_USER_DIR/analysis-list
cd /unix/cedar/egan/rebuild_contur_ref_area/myscan00/13TeV/0009
Herwig read herwig.in -I /unix/cedar/egan/rebuild_contur_ref_area/RunInfo -L /unix/cedar/egan/rebuild_contur_ref_area/RunInfo;
Herwig run herwig.run --seed=101  --tag=runpoint_0009  --numevents=30000 ;
