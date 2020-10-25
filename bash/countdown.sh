#!/bin/bash

# Let the user know we are reading in the number of times to run
echo "We are counting down to 0 from a number! What number do you want us to count down from?"

# Read in the number from the user. 
read inputNumber

# We want to make sure that the input was a number, otherwise the for loop doesn't work right
# We compare the read input variable to make sure that all characters are a number
# If this isn't true, then we want the if statement to run, so we add the ! to the statement to reverse when it runs
if ! [[ "$inputNumber" =~ ^[0-9]+$ ]] ; then
	echo "ERROR: Input was not a number. Try again"
	exit 1	
fi

# If the input was a number, we will get to the looping portion now
# We still have the issue where the inputNumber variable is being read as a string instead of a number
# To fix this, we need to use the eval command to convert the string to an integer
# We also use the echo command to print the value of $inputNumber since we don't know it
# We start at inputNumber and count down to 1
for i in $(eval echo {$inputNumber..1})
do
	# Output the phrase and the number of the loop we are running so that we know how far along the run is
	echo "Counting down from $inputNumber: $i!"
done