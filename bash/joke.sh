#! /bin/bash

# Outputs the options for the user to respond to knock knock joke.
echo "Knock Knock"
echo "Choose a response:"
echo "A - Who's there?"
echo "B - What?"
echo "C - Go away"
# Read the users choice of A, B or C
read response
# User chose option A, continue on with joke
if [ "A" = $response ]; then
		# Display the next part of the joke and read in the user's next response
        echo "Mustache"
        echo "Choose a response:"
        echo "A - Mustache?"
        echo "B - Mustache who?"
        echo "C - What?"
        read response2
		# User chose option B, finish the joke
        if [ "B" = $response2 ]; then
                echo "I mustache you a question, but I’ll shave it for later."
        # User didn't choose the expected option
		else
                echo "You're supposed to say [Mustache who?] Try again!"
        fi
# User chose an option that wasn't [Who's there? (A)], don't tell the joke
else
        echo "You're supposed to say [Who's there?] Try again!"
fi