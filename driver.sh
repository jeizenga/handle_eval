#!/usr/bin/env bash

INPUT_DIR=extra-disk/mutilated/
OUTPUT_DIR=erik_out/
BAD_DUMP=extra-disk/bad_gfas/

RUN="1"
while [ $RUN != "0" ]
do
	./scaledUpDataCollection.py -i $INPUT_DIR -o $OUTPUT_DIR 2> err.txt
	RUN=$?
	cat err.txt 1>&2
	if [ $RUN != "0" ]
	then
		LASTLINE=$(grep "testing on" err.txt | tail -n1)
		for TOKEN in $LASTLINE
		do
			if [ $TOKEN != "testing" ] && [ $TOKEN != "on" ]
			then
				mv $INPUT_DIR/$TOKEN $BAD_DUMP
			fi
		done
	fi
done

# get the header
for OUTFILE in $OUTPUT_DIR/*
do
	head -n1 $OUTFILE > handle_profiling.tsv
	break
done

# get below the header for everything
for OUTFILE in $OUTPUT_DIR/*
do
	tail -n +2 $OUTFILE >> handle_profiling.tsv
done
