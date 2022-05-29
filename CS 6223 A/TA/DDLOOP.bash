#!/bin/bash

LOOP=20         #How many times this will loop
SIZE=1024       #Size of file we're reading and writing to

#Repeat the command by {LOOP} number of times
for i in $(seq 1 $LOOP)
do
    #Use the DD command 
    #Take the 3rd line of output only and output it to a temporary file.  This records the end result data.
    dd bs=$SIZE count=$SIZE if=/dev/zero of=file.txt 2>&1 | head -n 3 | tail -n 1 &>> temp.txt

done

#Replace every , with a tab.  This is just for cleaner formatting.
#Output it to a file called results.txt to hold all our information.
sed 's/,/\t/g' temp.txt >> results.txt

#Delete the temp file.
rm temp.txt
