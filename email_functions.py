from datetime import datetime


# An email object stores values from the "From", "Subject", and "Date" fields of exported mbox
class Email:
    def __init__(self, from_field, subject_field, date_field):
        self.__from = from_field
        self.__subject = subject_field
        self.__date = date_field

    def get_from(self):
        return self.__from

    def get_subject(self):
        return self.__subject

    def get_date(self):
        return self.__date

    def get_datetime(self):
        # Datetime format:
        # Tue, 10 Sep 2013 10:05:45 -0600
        #  |   |  |   /   /  /  /   /
        # '%a, %d %b %Y %H:%M:%S %z'
        return datetime.strptime(self.__date, '%a, %d %b %Y %H:%M:%S %z')

    def get_domain(self):
        line = self.__from.split()
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

        return domain

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
