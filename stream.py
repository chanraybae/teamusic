import tkinter
from tkinter import *

# main
stream = Tk()
stream.title("Teamusic")    # window title
stream.geometry("1000x900")    # fixed window size
stream.configure(background="black")   # aesthetic choice


# adding logo
logo = PhotoImage(file="logo.png")
logo = logo.resize((100, 100))
Label(stream, image=logo, bg="black") .grid(row=0, column=0, sticky=W)

# creating song search query
Label(stream, text="Search for song: ", bg="black", fg="orange", font="none 12 bold") .grid(row=1, column=0, sticky=W)

stream.mainloop()


def choose_song():
    return -1


if __name__ == '__main__':
    print('PyChar')
