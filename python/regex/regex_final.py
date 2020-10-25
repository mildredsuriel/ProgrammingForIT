import re

url_regex = r'^(http:\/\/www\.|ftp:\/\/|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$'
# At the start of the string, check for all allowed characters including a-z, A-Z, and special characters that are allowed. Only allow for this check to occur 64 times since that's the length
# limit of the local part. Then we place our @ sign and start a new group check. The length of the portion after the @ sign is limited to 256 characters, so we allow this many character checks
# The . portion of the email is optional, so we check to see if it is there, and if it is there we make sure that the website type is at least 2 characters since that's the minimum allowed (ex. ".co")
email_regex = "^[a-zA-Z0-9\"\.!_%+-]{1,64}@([a-zA-Z0-9-]{1,256})((\.?)[a-zA-Z]{2,63})"

# Function to check whether a regex matches a regex string, used to check both URL and EMAIL regexes
def check_valid_regex_string(regex_string, regex, line_number):
    # Use regex library to check our regex for a given string
    if(re.search(regex,regex_string)):
        print(str(line_number) + " : Valid String: " + regex_string.rstrip())
        return 1
    else:
        print(str(line_number) + " : Invalid String : " + regex_string.rstrip())
        return 0

if __name__ == '__main__' :

    print("--------------------------------------------------------")
    print("Testing Email REGEX " + str(email_regex))
    print("--------------------------------------------------------")

    # Keep track of how many emails are tested and valid in our valid_emails.txt
    valid_emails_count  = 0
    valid_emails_tested = 0

    # Keep track of how many emails are tested and invalid in our invalid_emails.txt
    invalid_emails_count  = 0
    invalid_emails_tested = 0

    # Open up the two files email files for validating our regex expression
    valid_emails_file   = open('valid_emails.txt', 'r')
    invalid_emails_file = open('invalid_emails.txt', 'r')

    print("\n---Valid email list---")
    # Go through each line of the valid emails file    
    for line in valid_emails_file:
        # each line should represent the email address to be checked
        email = line
        # Increment our counter for each line tested
        valid_emails_tested += 1
        # Call our function to check if the email is valid based on the regex used.
        # If it is valid, we want to increment our valid email counter
        if check_valid_regex_string(email, email_regex, valid_emails_tested):
            valid_emails_count += 1

    print("\n---Invalid email list---")
    # Go through each line of the invalid emails file    
    for line in invalid_emails_file:
        # each line should represent the email address to be checked
        email = line
        # Increment our counter for each line tested
        invalid_emails_tested += 1
        # Call our function to check if the email is valid based on the regex used.
        # If it is invalid, we want to increment our invalid email counter
        if not check_valid_regex_string(email, email_regex, invalid_emails_tested):
            invalid_emails_count += 1

    # Print out the ratio of correct email counts over the number tested to see how well our regex works
    print("Valid email matching : " + str(valid_emails_count) + "/" + str(valid_emails_tested))
    print("Invalid email matching : " + str(invalid_emails_count) + "/" + str(invalid_emails_tested) + "\n")

    # Close files once we are done using them
    valid_emails_file.close()
    invalid_emails_file.close()

    print("--------------------------------------------------------")
    print("Testing URL REGEX " + str(email_regex))
    print("--------------------------------------------------------")

    # Keep track of how many urls are tested and valid in our valid_urls.txt
    valid_urls_count  = 0
    valid_urls_tested = 0

    # Keep track of how many urls are tested and invalid in our invalid_urls.txt
    invalid_urls_count  = 0
    invalid_urls_tested = 0

    # Open up the two files url files for validating our regex expression
    valid_urls_file   = open('valid_urls.txt', 'r')
    invalid_urls_file = open('invalid_urls.txt', 'r')

    print("\n-----Testing Valid URLS-----\n")
    # Go through each line of the valid urls file    
    for line in valid_urls_file:
        # each line should represent the url address to be checked
        url = line
        # Increment our counter for each line tested
        valid_urls_tested += 1
        # Call our function to check if the url is valid based on the regex used.
        # If it is valid, we want to increment our valid url counter
        if check_valid_regex_string(url, url_regex, valid_urls_tested):
            valid_urls_count += 1

    print("\n----Testing Invalid URLS-----\n")
    # Go through each line of the invalid urls file    
    for line in invalid_urls_file:
        # each line should represent the url address to be checked
        url = line
        # Increment our counter for each line tested
        invalid_urls_tested += 1
        # Call our function to check if the url is valid based on the regex used.
        # If it is invalid, we want to increment our invalid url counter
        if not check_valid_regex_string(url, url_regex, invalid_urls_tested):
            invalid_urls_count += 1

    # Print out the ratio of correct url counts over the number tested to see how well our regex works
    print("\n")
    print("Valid url matching : " + str(valid_urls_count) + "/" + str(valid_urls_tested))
    print("Invalid url matching : " + str(invalid_urls_count) + "/" + str(invalid_urls_tested))

    # Close files once we are done using them
    valid_urls_file.close()
    invalid_urls_file.close()
