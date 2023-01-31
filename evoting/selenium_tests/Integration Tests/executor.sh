#!/bin/sh

for script in Test_Case_ID_?.py; do 
	python $script

done

for script in Test_Case_ID_??.py; do 
	python $script

done