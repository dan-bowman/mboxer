# Tkinter Functions
from tkinter import Tk, StringVar
# Tkinter Constants
from tkinter import BOTTOM, TOP, LEFT, RIGHT, BOTH, N, S, E, W, NE, NW, SE, SW, CENTER, X, Y
# Tkinter Styled Widgets
from tkinter.ttk import Frame, Label, Entry, Button, Notebook, OptionMenu
# pandas and matplotlib for statistics and plotting
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import mailbox
import csv
import sys
from datetime import datetime
from pandas import DataFrame, Series

from email_functions import Email



# THERE EXISTS NO DATE FIELD EXPORTED AS CSV FROM OUTLOOK
def run_through_csv(csv_file):
    with open(csv_file, mode='r') as file:
        emails = csv.DictReader(file)
        for email in emails:
            for mkey in email:
                print(mkey, ": ", email[mkey])
                input()


# For debug and dev
def run_through_mbox(mbox_file):
    emails = mailbox.mbox(mbox_file)

    email_list = []

    email_data = {"from": [],
                  "subject": [],
                  "domain": [],
                  "date": [],
                  "content": []}

    for key in emails.iterkeys():
        message = emails[key]
        body = None
        content_type = message.get_content_type()
        # Check for multipart content type here
        multipart = message.is_multipart()
        if multipart:
            for part in message.walk():
                if part.is_multipart():
                    for subpart in part.walk():
                        if not subpart.is_multipart():
                            content = "\n" + get_message_body(subpart, subpart.get_content_type()) + "\n"
                            if body is not None:
                                body += content
                            else:
                                body = content
                else:
                    content = "\n" + get_message_body(part, part.get_content_type()) + "\n"
                    if body is not None:
                        body += content
                    else:
                        body = content
        else:
            body = get_message_body(message, content_type)

        email_obj = Email(message['From'], message['Subject'], message['Date'], body)
        email_list.append(email_obj)

    subject_data = []
    from_data = []
    domain_data = []
    date_data = []
    content_data = []
    for e in email_list:
        subject_data.append(e.get_subject())
        from_data.append(e.get_email_address())
        domain_data.append(e.get_domain())
        date_data.append(e.get_date())
        content_data.append(e.get_body_content())

    # Create the data dictionary
    data = {'Subject': subject_data,
            'From': from_data,
            'Domain': domain_data,
            'Date': date_data,
            'Content': content_data}

    # Create the dataframe
    df = DataFrame(data)


    # Make a pandas series for the domains so they can be counted
    domain_series = Series(df.Domain)

    # DataFrame for domain name count histogram
    df_domain_hist = DataFrame(domain_series.value_counts())

    # Make a pandas series for the senders' full email addresses so they can be counted
    from_series = Series(df.From)

    # DataFrame for email address count histogram
    df_from_hist = DataFrame(from_series.value_counts())

    print(df_from_hist)
    print(df_domain_hist)

def get_message_body(message, content_type):
    body = None
    if content_type in ('text/plain', 'text/html'):
        body = message.get_payload()
    if body is None:
        body = ""
    return body

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


## create progress bar
# progress = ttk.Progressbar(master, orient = HORIZONTAL, length = 120)
## pack progress bar into master
# progress.pack()
## to step progress bar up
# progress.config(mode = ‘determinate’,maximum=100, value = 5)
# progress.step(5)

class GUI(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_frames()
        self.master.title("Tk with Pandas Plot test")

    def create_frames(self):
        self.tabs = Notebook(self)
        self.tabs.pack()

        self.home_frame = HomeFrame(self.tabs)

        self.tabs.add(self.home_frame, text='Home')

        self.tabs.select(self.home_frame)
        self.tabs.enable_traversal()

    def start(self):
        self.master.mainloop()


class HomeFrame(Frame):
    def __init__(self, master=None):
        super().__init__(master, padding='0.5i')
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.change_label = Label(self, text='Change this value.')
        self.change_entry = Entry(self)
        self.change_button = Button(self, command=self.add_plot_frame)

        self.change_label.pack(side=TOP)
        self.change_entry.pack(side=TOP)
        self.change_button.pack(side=TOP)

    def add_plot_frame(self):
        plot_frame = PlotFrame(self.master)
        if plot_frame.plot is not None:
            plot_frame.plot.graph.get_tk_widget().pack_forget()
        plot_frame.create_plot(self.change_entry.get(), plot_frame.data_frame, plot_frame, plot_frame.option_var)
        self.master.add(plot_frame, text=self.change_entry.get())
        self.master.select(plot_frame)


class PlotFrame(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.plot_title = ''
        self.create_widgets()

    def create_widgets(self):
        self.dropdown_label = Label(self, text='Choose a type of graph')

        self.option_var = StringVar(self, name="option")
        self.option_var.set('Bar')
        self.option_var.trace('w', self.on_option_change)

        self.close_button = Button(self, text='Close Tab', command=self.close_tab)

        self.data = {'Country': ['US', 'CA', 'GER', 'UK', 'FR'],
                     'GDP_Per_Capita': [45000, 42000, 52000, 49000, 47000]}
        self.data_frame = DataFrame(self.data)

        # self.plot = self.create_plot(self.plot_title, self.data_frame, self, self.option_var)
        self.plot = None

        self.options = ['Bar', 'Line']
        self.dropdown = OptionMenu(self, self.option_var, self.options[0], *self.options)

        self.close_button.pack(anchor=W)
        self.dropdown_label.pack(side=TOP, anchor=N)
        self.dropdown.pack(side=TOP, anchor=N)

    def on_option_change(self, *args):
        if args[0] == 'option' and self.plot is not None:
            self.plot.graph.get_tk_widget().pack_forget()
            self.plot.plot_graph(self, self.option_var)

    def create_plot(self, title, data_frame, master, option_var):
        self.plot = Plot(title, data_frame, master, option_var)

    def close_tab(self):
        self.master.forget(self)


class Plot:
    def __init__(self, title, data_frame, master, option_var):
        self.title = title
        self.data_frame = data_frame

        self.plot_graph(master, option_var)

    def plot_graph(self, master, option_var, size=(7, 6), subplot=111):
        self.figure = plt.Figure(figsize=size, dpi=100)
        self.axis = self.figure.add_subplot(subplot)
        self.graph = FigureCanvasTkAgg(self.figure, master)
        self.axis.set_title(self.title)
        self.graph.get_tk_widget().pack(side=RIGHT, anchor=S, fill=X)
        self.data_frame.plot(kind=option_var.get().lower(), legend=True, ax=self.axis)


def main():
    # Print all the Email objects' str() conversions
    #mail = load_mbox(sys.argv[1])
    run_through_mbox('E:/email/archive/dbowman1000.mbox')
    #for m in mail:
    #    print(m)
    #root = Tk()
    #gui = GUI(master=root)
    #gui.start()


main()
