#!/bin/bash
function print_header(){
    printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
    echo $1
    printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
}

# Directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" 

# Virtualenv
cd $DIR
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt

# Comment for using GPU
export CUDA_VISIBLE_DEVICES=-1

# Begin experiment (2-Player IPD)
cd $DIR
for seed in {1..1}
do
    python3.6 main.py \
    --env-name "wolfpack-v0" \
    --seed $seed \
    --prefix ""
done
