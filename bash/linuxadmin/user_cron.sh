# Get a list of all of the users for the new hourly snapshot
compgen -u > users_new_hourly

# Compare the new hourly snapshot to the previous hour snapshot
diff users_last_hourly users_new_hourly > user_changes

# Check if the file is empty. If the string returned from the find command is empty, it means that the file being looked at isn't empty, signifying their are user changes
if [ -z "$(find -empty -name user_changes)" ]
then
    echo "User changes detected!"
    file=$(date +"%m_%d_%Y_H%H_user_changes")
    # Print all but the first and last lines since they don't contain the username changes, and save it to an hourly snapshot file
    sed '1d;$d' user_changes | tee $file
# Otherwise if the string returned is empty, then there are no differences
else
    echo "No user changes detected."
fi

cp users_new_hourly users_last_hourly