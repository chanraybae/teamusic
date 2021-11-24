import tkinter
from tkinter import *
from PIL import Image, ImageTk


# defines which song shall be chosen
def choose_song():
    return -1


if __name__ == '__main__':
    stream = Tk()
    stream.title("Teamusic")  # window title
    stream.geometry("1450x1025")  # fixed window size
    stream.configure(background="black")  # aesthetic choice

    # adding logo
    Label(stream, text="\n\n\n\n\n\n\t teamusic", bg="black", fg="white", font="{Apple LiGothic} 10 bold") \
        .grid(row=0, column=0, padx=7, pady=0, sticky=W)
    logo_orig = Image.open("logo.jpg")
    resize_logo = logo_orig.resize((100, 75))
    logo = ImageTk.PhotoImage(resize_logo)
    Label(stream, image=logo, bg="black").grid(row=0, column=0, padx=50, pady=0, sticky=W)

    # creating song search query
    Label(stream, text="\n\n\nSearch for song  ", bg="black", fg="white", font="{Apple LiGothic} 18 bold") \
        .grid(row=0, column=5, padx=8, pady=50, sticky=W)
    # welcoming user to program in app
    Label(stream, text="Welcome, Thomas", bg="black", fg="white", font="{Apple LiGothic} 18 bold") \
        .grid(row=1, column=5, padx=8, pady=20, sticky=W)

    # creating search box
    searchbar = Entry(stream, width=70, bg="white", font="{Apple LiGothic} 18")
    searchbar.grid(row=0, column=5, padx=8, pady=50, sticky=W)


    stream.mainloop()

    print('PyChar')
