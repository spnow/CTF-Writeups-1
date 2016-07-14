#!/bin/bash

usage ()
{
    echo Parallel sort
    echo usage: psort file1 file2
    echo Sorts text file file1 and stores the output in file2
}

# test if we have two arguments on the command line
if [ $# != 2 ]
then
    usage
    exit
fi

pv $1 | parallel --pipe --files sort -S512M | parallel -Xj1 sort -S1024M -m {} ';' rm {} > $2