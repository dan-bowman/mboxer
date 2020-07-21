import mailbox
import csv
import sys
from datetime import datetime
from email_functions import Email


# THERE EXISTS NO DATE FIELD EXPORTED AS CSV FROM OUTLOOK
def run_through_csv(csv_file):
    with open(csv_file, mode='r') as file:
        emails = csv.DictReader(file)
        for email in emails:
            for mkey in email:
                print(mkey, ": ", email[mkey])
                input()


# For debug
def run_through_mbox(mbox_file):
    emails = mailbox.mbox(mbox_file)
    for key in emails.iterkeys():
        message = emails[key]

        for mkey in message:
            print(mkey, ": ", message[mkey])
            input()


# Creates a list of Email objects based on the mbox file
def load_mbox(mbox_file):

    # Initialize email_list, add email objects to this list
    email_list = []

    # Iterate the mbox email list and append each Email object to the list
    emails = mailbox.mbox(mbox_file)
    for key in emails.iterkeys():
        message = emails[key]
        email_list.append(Email(message['From'], message['Subject'], message['Date']))

    return email_list


def main():
    # Print all the Email objects' str() conversions
    mail = load_mbox(sys.argv[1])
    for m in mail:
        print(m)


main()
