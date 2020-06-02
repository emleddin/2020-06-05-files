#!/bin/bash
#PBS -q FIXME                       # queue allocation
#PBS -l nodes=1:ppn=20,mem=20GB     # 20 processors
#PBS -j oe                          # same output and error file
#PBS -r n                           # Job not re-runnable
#PBS -o OpenMM.err                  # name of error file
#PBS -N 5Y2S_CPU_OpenMM             # name of job for queue

## If you get a segfalt error and you're a TINKER user
## add the .bashrc_blank file to $HOME on Cruntch and 
## uncomment this line.
#source ~/.bashrc_blank

## Go to the directory that the job was submitted from
cd $PBS_O_WORKDIR

## Use the 20 CPUs we requested
export OPENMM_CPU_THREADS=20

## Load OpenMM
module load openmm/cuda-8.0

## Run the Python Script and print Terminal output to file
python new_openmm_simulations.py
