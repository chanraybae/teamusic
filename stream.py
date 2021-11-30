import tkinter
from playsound import playsound
from tkinter import *
from PIL import Image, ImageTk


# defines which song shall be chosen
def choose_song():
    return -1

# collects the text put into the search bar
#def searchquery():
    #entered_text = searchbar.get()

def play(playlist, song_name):
    chosen_song = playlist[song_name]
    playsound(chosen_song)


if __name__ == '__main__':
    # creating our hash table of songs
    library = {
        'Through and Through': 'thru.mp3'
    }

    # using tkinter to create our GUI
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
        .grid(row=0, column=1, padx=8, pady=50, sticky=W)
    # welcoming user to program in app
    Label(stream, text="Welcome, Thomas", bg="black", fg="white", font="{Apple LiGothic} 18 bold") \
        .grid(row=1, column=1, padx=8, pady=20, sticky=W)

    # creating search box
    searchbar = Entry(stream, width=70, bg="white", font="{Apple LiGothic} 18")
    searchbar.grid(row=0, column=1, padx=8, pady=50, sticky=W)

    # play button for songs
    # Khai Dreams Song
    thru_cover_orig = Image.open("thru.png")
    resize_thru_cover = thru_cover_orig.resize((500, 300))
    thru_cover = ImageTk.PhotoImage(resize_thru_cover)
    # creating label for button event
    thru_label = Label(image=thru_cover)
    # button to play in library
    thru_button = Button(stream, image=thru_cover, command=lambda: play(library, "Through and Through")) \
        .grid(row=2, column=1, padx=7, pady=100, sticky=W)

    stream.mainloop()

    print('PyChar')
    print('hi')
