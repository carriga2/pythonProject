from tkinter import *
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import csv


class App(Frame): # App is name of the class

    def __init__(self, master=None): # inheriting from class Frame
        Frame.__init__(self, master)

        self.filename = None

        # list to store data in memory
        self.datalist = []

        # currently displayed record
        self.currentindex = 0

        self.mainframe = Frame()
        Label(self.mainframe, text="ID:").grid(column=0, row=0, sticky="W")
        self.firstname_entry = Entry(self.mainframe, width=30)
        self.firstname_entry.grid(column=1, row=0, sticky="W")

        Label(self.mainframe, text="Booker Name:").grid(column=0, row=1, sticky="W")
        self.lastname_entry = Entry(self.mainframe, width=30)
        self.lastname_entry.grid(column=1, row=1, sticky="W")

        Label(self.mainframe, text="Room Name:").grid(column=0, row=2, sticky="W")
        self.address_entry = Entry(self.mainframe, width=30)
        self.address_entry.grid(column=1, row=2, sticky="W")

        Label(self.mainframe, text="From Date:").grid(column=0, row=3, sticky="W")
        self.phone_entry = Entry(self.mainframe, width=30)
        self.phone_entry.grid(column=1, row=3, sticky="W")

        Label(self.mainframe, text="Until Date:").grid(column=0, row=4, sticky="W")
        self.email_entry = Entry(self.mainframe, width=30)
        self.email_entry.grid(column=1, row=4, sticky="W")

        self.add_button = Button(self.mainframe, text="Add", width=12, command=self.add_record)
        self.add_button.grid(column=2, row=0, padx=5)

        self.delete_button = Button(self.mainframe, text="Delete", width=12, command=self.delete_record)
        self.delete_button.grid(column=2, row=1, padx=10)

        self.update_button = Button(self.mainframe, text="Update", width=12, command=self.update_record)
        self.update_button.grid(column=2, row=2, padx=10)

        self.save_as_button = Button(self.mainframe, text="Save As...", width=12, command=self.save_as)
        self.save_as_button.grid(column=2, row=3, padx=10)

        self.save_button = Button(self.mainframe, text="Save", width=12, command=self.save)
        self.save_button.grid(column=2, row=4, padx=10)

        self.openfile_button = Button(self.mainframe, text="Open File...", width=12, command=self.readfile)
        self.openfile_button.grid(column=2, row=5, padx=10)

        self.mainframe.pack(side=TOP) # putting mainframe onto top side of office tool

        names = ["First", "Previous", "Next", "Last"]
        self.nav_buttons = []
        self.navFrame = Frame()
        # The lambda values are  0 = First, 1 = Previous 2 = Next, 3 = Last
        for item in range(0, len(names)):
            b = Button(self.navFrame, text=names[item], bg="steelblue", fg="white", width=12, # creates the buttons
                       command=lambda i=item: self.check_navigation(i))
            self.nav_buttons.append(b) # added to nav buttons
            self.nav_buttons[item].grid(row=0, column=item, padx=2, pady=4) # positioning the buttons

        self.navFrame.pack(side=BOTTOM) # places the buttons at the bottom of the screen

    def add_record(self):  # reads data from GUI and adds each record to datalist[]
        #   adds record to datalist
        print(self.firstname_entry.get(), self.lastname_entry.get(),     # prints out new record which has just been added
              self.address_entry.get(), self.phone_entry.get(), self.email_entry.get())

        record = (self.firstname_entry.get(), self.lastname_entry.get(),   # local record variable
                  self.address_entry.get(), self.phone_entry.get(), self.email_entry.get())

        self.datalist.append(record)  # adds record
        self.currentindex = len(self.datalist) - 1              # subtract 1 and it gives us our last record
        print(self.datalist)
        mb.showinfo("Record Added", "One Record Added")  # printing Message Box
        self.clear_entries()

    def delete_record(self):
        try:
            del self.datalist[self.currentindex]   # del keyword used to delete, does not update, have to click update
            self.display(self.currentindex)
        except Exception:
            mb.showinfo("Nothing to delete", "No Record Found")  # Message box

    def update_record(self):  # similar to add record
        # line below gets data from entries on GUI
        record = (self.firstname_entry.get(), self.lastname_entry.get(),
                  self.address_entry.get(), self.phone_entry.get(), self.email_entry.get())
        # assign record to the datalist
        self.datalist[self.currentindex] = record
        print(self.datalist[self.currentindex]) # does not save data, must click save button

    def check_navigation(self, value):
        if value == 0:  # first _button
            self.currentindex = 0
        elif value == 1:  # previous _button
            self.currentindex -= 1  # reduce the index
        elif value == 2:  # next _button
            self.currentindex += 1   # increases the index
        elif value == 3:  # last _button
            self.currentindex = len(self.datalist) - 1   # gets length of the datalist -1
        else:  # just in case!
            self.currentindex = 0   # 0 displays the first record

        self.display(self.currentindex)

    def display(self, index):
        self.clear_entries()  # clears tx boxes

        if index < 0:
            index = 0

        if index >= (len(self.datalist) - 1):
            index = (len(self.datalist) - 1)

        row = self.datalist[index]   # puts records from file and into the display
        self.firstname_entry.insert(0, row[0])
        self.lastname_entry.insert(0, row[1])
        self.address_entry.insert(0, row[2])
        self.phone_entry.insert(0, row[3])
        self.email_entry.insert(0, row[4])

        self.currentindex = index

    def clear_entries(self):    # clears the text boxes
        self.firstname_entry.delete(0, END)
        self.lastname_entry.delete(0, END)
        self.address_entry.delete(0, END)
        self.phone_entry.delete(0, END)
        self.email_entry.delete(0, END)

    def save_as(self):
     #    displays the dialog box
        self.filename = fd.asksaveasfilename(defaultextension=".csv",   # defaults to csv
                                             filetypes=[("csv files", ".csv"), ("all files", ".*")])
        self.writefile()  # saves the records

    def save(self):
        if self.filename is None or self.filename == "":
            self.save_as()
        else:
            self.writefile()

    def writefile(self):

        if len(self.datalist) > 0:
            csvfile = open(file=self.filename, mode='w', newline='\n')
            writer = csv.writer(csvfile, delimiter=",")

            for lcv in range(0, len(self.datalist)):
                writer.writerow(self.datalist[lcv])  # writes the file

            csvfile.close()  # close file after to write it

        else:
            print("Nothing to save")

    def readfile(self):   #   opens the file

        self.datalist.clear()
        self.filename = fd.askopenfilename(defaultextension=".csv",
                                           filetypes=[("csv files", ".csv"), ("all files", ".*")])
        csvfile = open(self.filename, 'r')
        reader = csv.reader(csvfile, delimiter=',')

        for line in reader:
            print(tuple(line))
            self.datalist.append(line)

        self.display(0)  # display first record
        csvfile.close()
        self.currentindex = 0
        print(self.datalist)

if __name__ == "__main__":
    root = Tk() # creating tk object, creating window
    root.title("Office Booking Tool")
    root.geometry("400x200+0+0")
    app = App(master=root)  # call constructor
    app.mainloop()
