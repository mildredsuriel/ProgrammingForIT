#! /bin/bash

# Ask what the user would like for lunch and output their options
echo "What would you like for lunch?"
echo "A - Chipotle"
echo "B - Mcdonalds"
echo "C - Subway"
# Read in user selection
read selection
# They chose chipotle, give Chipotle food options
if [ "A" = $selection ]; then
		# Display food options and take in user's next selection
        echo "Chipotle it is!"
        echo "Cashier: What are you getting?"
        echo "A - Burrito"
        echo "B - Salad"
        echo "C - Bowl"
        read selection
		# User chose a burrito
        if [ "A" = $selection ]; then
                echo "One burrito coming up!"
		# User chose a salad 
        elif [ "B" = $selection ]; then
                echo "One salad coming up!"
		# User chose a bowl
        elif [ "C" = $selection ]; then
                echo "Three tacos coming up!"
        # User chose something that wasn't listed
		else
                echo "We don't have that product, sorry"
        fi
# They chose Mcdonalds, give Mcdonalds food options
elif [ "B" = $selection ]; then
		# Display food options and take in user's next selection
        echo "Mcdonalds it is!"
        echo "Cashier: What are you getting?"
        echo "A - Burger"
        echo "B - Chicken Sandwich"
        echo "C - Chicken Nuggets"
        read selection
		# User chose a burger
        if [ "A" = $selection ]; then
                echo "One burger coming up!"
		# User chose a chicken sandwich
        elif [ "B" = $selection ]; then
                echo "One chicken sandwich coming up!"
		# User chose chicken nuggets
        elif [ "C" = $selection ]; then
                echo "Chicken nuggets coming up!"
        else
		# User chose something that wasn't listed
                echo "We don't have that product, sorry"
        fi

elif [ "C" = $selection ]; then
        echo "Subway it is!"
        echo "Cashier: What are you getting?"
