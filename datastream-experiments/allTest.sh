#!/bin/bash
runTest () {
		n=$1
		b=$2
		d=$3
		./runTest.sh --direction $d -b $b -n $n -a custom
		sleep 3
}
for d in "in" "out"
do
	for n in 1  
	do
		for b in {1..35} 
	       	do
			runTest $n $b $d
		done
	done
done

