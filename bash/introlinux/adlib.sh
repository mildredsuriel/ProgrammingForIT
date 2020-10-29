# Use the built in date command and format it, saving it to the variable DATE
DATE=$(date +"%b-%d-%y")
# Create a file with the date saved to the variable DATE
touch $DATE
# Print text to the screen
echo "May I know your name please?"
# Read in input from the user an save it to a variable yourname
read yourname
# Print more text, calling the variable that was read in
echo "Good Day $yourname"

echo "We're going to play a Mad Lib. Enter the following type of words:"
# Read in each variable after describing what is is
echo "Adjective: "
read adjective1
echo "Noun Plural: "
read nounplural1
echo "Adjective: "
read adjective2
echo "Noun Plural: "
read nounplural2
echo "Verb Base Form: "
read verbbaseform1
echo "Noun Plural: "
read nounplural3
echo "Noun: "
read noun1
echo "Animal: "
read animal1
echo "Verb Past Tense: "
read verbpasttense1
echo "Part of Body: "
read partofbody1

# Print out the story, filling in the read variables into the mad lib portions of the story
echo "One day Columbus was at a dinner which a $adjective1 gentleman had given in his honor, and several persons were present"
echo "who were jealous of the great admiral's $nounplural1. They were proud, conceited fellows, and they very soon began to try"
echo "to make Columbus uncomfortable."

echo "You have discovered $adjective0 $nounplural2 beyond the seas, they said, but what of that? We do not see why there should"
echo "be so much said about it. Anybody can sail across the ocean - and anybody can $verbbaseform1 the $nounplural3 with a $noun1,"
echo "just as you have done. It is the simplest thing in the world."

echo "Columbus made no answer - but after a while he took a $animal1 and said to the company 'Who among you, gentlemen, can make this"
echo "$animal1 stand on end?' One by one those at the table tried the experiment. When the $animal1 had gone entirely around and none"
echo "had succeeded, all said that it could not be done."

echo "Then Columbus took the $animal1 and $verbpasttense1 its $partofbody1 gently. After that there was no trouble in making it stand on end."

echo "Gentleman, said he, what is easier than to do this which you said was impossible? It is the simplest thing in the world."
echo "Anybody can do it - AFTER he has been shown how!"
