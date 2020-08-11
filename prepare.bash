#!/bin/bash

cmake build  -B./FocusedSampling -S./FocusedSampling/ -DCMAKE_BUILD_TYPE=Release

cmake --build ./FocusedSampling

#get data set
FILE=FocusedSampling/data/table/forest_data_normalised.csv
if [ -f "$FILE" ]; then
    echo "$FILE already exists."
else 
    wget -P FocusedSampling/data/table/ wwwdb.inf.tu-dresden.de/misc/ForestData/forest_data_normalised.csv
fi


FILE=ConditionalSampling/forest.csv
if [ -f "$FILE" ]; then
    echo "$FILE already exists."
else 
    wget -P ConditionalSampling/ wwwdb.inf.tu-dresden.de/misc/ForestData/forest.csv
fi

FILE=ConditionalSampling/buildCondSample/cond_sample_7q.pkl
if [ -f "$FILE" ]; then
    echo "$FILE already exists."
else 
    wget -P ConditionalSampling/buildCondSample wwwdb.inf.tu-dresden.de/misc/ForestData/cond_sample_7q.pkl
fi

FILE=ConditionalSampling/buildCondSample/cond_sample_5q.pkl
if [ -f "$FILE" ]; then
    echo "$FILE already exists."
else 
    wget -P ConditionalSampling/buildCondSample wwwdb.inf.tu-dresden.de/misc/ForestData/cond_sample_5q.pkl
fi

FILE=ConditionalSampling/buildCondSample/cond_sample_3q.pkl
if [ -f "$FILE" ]; then
    echo "$FILE already exists."
else 
    wget -P ConditionalSampling/buildCondSample wwwdb.inf.tu-dresden.de/misc/ForestData/cond_sample_3q.pkl
fi

echo 'Conditional Sampling: Please run python3 evalCondSample'
echo 'Focused Sampling: cd FocusedSampling/bin ./main'
