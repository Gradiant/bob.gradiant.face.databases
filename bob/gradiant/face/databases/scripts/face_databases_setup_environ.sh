#!/bin/bash

declare -a databases=("REPLAY_ATTACK_PATH=$1"
                      "REPLAY_MOBILE_PATH=$2"
		              "MSU_MFSD_PATH=$3"
                      "OULU_NPU_PATH=$4"
		              "HOLYFACE_PATH=$5"
		              "UVAD_PATH=$6"
                     )

for path in "$@"
do
	if [[ -d $path ]]; then
	    : 
	else
	    echo "IOError: Directory $path does not exist."
	    exit 1
	fi
done


for env in "${databases[@]}"
do
   echo export $env >> ~/.bashrc
done

printf ">> Done! These are the chosen values:"
printf "\n--------------------------------------\n"
echo "REPLAY_ATTACK_PATH : $1"
echo "REPLAY_MOBILE_PATH : $2"
echo "MSU_MFSD_PATH : $3"
echo "OULU_NPU_PATH : $4"
echo "HOLYFACE_PATH : $5"
echo "UVAD_PATH : $6"
echo "--------------------------------------"
printf ">> Remember to activate your conda env again.\n"

exec bash
