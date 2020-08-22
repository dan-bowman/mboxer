from datetime import datetime
from numpy import isnan


# An email object stores values from the "From", "Subject", and "Date" fields of exported mbox
class Email:
    def __init__(self, from_field, subject_field, date_field, content_field):
        self.__from = from_field
        self.__subject = subject_field
        self.__date = date_field

        line = str(self.__from).split()
        email_address = line[-1].strip('<').strip('>')

        # Store whatever is after the @ symbol in the From field
        full_domain = email_address[email_address.index("@") + 1:].lower()

        # Split on the dots
        split_domain = full_domain.split('.')

        # Initialize short form domain
        domain = ""
        if split_domain[-2] == "co":
            domain = split_domain[-3] + "." + split_domain[-2] + "." + split_domain[-1]
        else:
            domain = split_domain[-2] + "." + split_domain[-1]

        self.__email_address = email_address
        self.__domain = domain
        self.__content = content_field

    def get_from(self):
        return self.__from

    def get_subject(self):
        return self.__subject

    def get_date(self):
        return self.__date

    def get_datetime(self):
        # Tue, 10 Sep 2013 10:05:45 is 25 characters
        mod_date = str(self.__date)[:26]
        d = datetime.strptime(mod_date, '%a, %d %b %Y %H:%M:%S')
        return d

    def get_domain(self):
        return self.__domain

    def get_email_address(self):
        return self.__email_address
    
    def get_body_content(self):
        return self.__content

    def __str__(self):
        return 'Domain: ' + self.get_domain() + '\nSubject: ' + self.get_subject() + '\n\tDate: ' + self.get_date() + '\n'


# Create subclasses here to help implement csv support
class MboxEmail(Email):
    def __init__(self):
        super().__init__()
    pass


class CsvEmail(Email):
    def __init__(self):
        super().__init__()
    pass
