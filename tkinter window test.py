import tkinter as tk
import threading
import pygame
from pygame import mixer
from tkinter import *
from PIL import Image, ImageTk

############################################

# this function displays the search results after hitting
# the search button
def display_search(playlist, search, album_button, buttonArr, targ_frame):
    album_button.grid_remove()
    i = 0
    j = 0
    for j in range(4):
        for i in range(len(playlist)):
            if (buttonArr[j][i]!=0):
                buttonArr[j][i].grid_remove()
            i = i + 1
        j=j+1
    i = 0
    search = search.lower()
    for key in playlist:
        lower_song= key.lower()
        if search in lower_song:
            buttonArr[0][i] = Button(targ_frame, text=key, width=20,command=lambda song=key:play_thread(library, song), font="{Apple LiGothic} 12 bold")
            buttonArr[0][i].grid(row=2 + i, column=1, padx=5, pady=10, sticky=W)
            buttonArr[1][i] = Button(targ_frame, text="Play Next", width=8, font="{Apple LiGothic} 9")
            buttonArr[1][i].grid(row=2 + i, column=2, padx=5, pady=10, sticky=W)
            buttonArr[2][i] = Button(targ_frame, text="Add to Queue", width=8, font="{Apple LiGothic} 9")
            buttonArr[2][i].grid(row=2 + i, column=3, padx=5, pady=10, sticky=W)
        i = i + 1

############################################

def play(playlist, song_name):
    chosen_song = playlist[song_name]
    mixer.music.load(chosen_song)
    mixer.music.play()

def play_thread(libray, song):
    t = threading.Thread(target=play, args=(library, song))
    t.start()

def playorpause():
    if pygame.mixer.music.get_busy():
        mixer.music.pause()
    else:
        mixer.music.unpause()

############################################

# library of songs
library = {
    'Through and Through': 'thru.mp3',
    'Adore You': 'adoreyou.mp3',
    'Love Me Back': 'lovemeback.mp3'
}

# button array for search results
buttonArr1 = [[0 for x in range(4)] for x in range(4)]
buttonArr2 = [[0 for x in range(4)] for x in range(4)]
buttonArr3 = [[0 for x in range(4)] for x in range(4)]
buttonArr4 = [[0 for x in range(4)] for x in range(4)]

############################################

# create the tkinter window and initialize the pygame audio mixer
stream = Tk()
stream.title("Teamusic Split View")  # window title
stream.geometry("1450x1025")  # window dimensions
stream.configure(background="black")

mixer.init()

############################################

# preparing images for inclusion in GUI

# setting up the teamusic image logo
logo_orig = Image.open("logo.jpg")
resize_logo = logo_orig.resize((25,19))
logo = ImageTk.PhotoImage(resize_logo)

# setting up the play/pause button
playpause_orig = Image.open("playpause.png")
resize_playpause = playpause_orig.resize((25, 19))
playpause = ImageTk.PhotoImage(resize_playpause)

# Khai Dreams Through and Through
thru_cover_orig = Image.open("thru.png")
resize_thru_cover = thru_cover_orig.resize((250,150))
thru_cover= ImageTk.PhotoImage(resize_thru_cover)

############################################

# frame 1

frame1 = LabelFrame(stream, width=725, height=400, text="User 1", bg="black", fg="white")
frame1.grid(row=0, column=0, sticky=W)
frame1.grid_propagate(0)

# teamusic logo
logolabel1 = Label(frame1, image=logo, bg="black")
logolabel1.grid(row=0, column=0, padx=5, pady=5)
label1 = Label(frame1, text="teamusic", bg="black",
             font="{Apple LiGothic} 6 bold", fg="white")
label1.grid(row=1, column=0, padx=5, pady=5)

# Welcome, Thomas
welcome1 = Label(frame1, text="Welcome, Thomas", bg="black", fg="white", font="{Apple LiGothic} 9 bold")
welcome1.grid(row=1, column=1, padx=5, pady=5, sticky=W)

# search bar and button
searchbar1 = Entry(frame1, width=35, bg="white", font="{Apple LiGothic} 9")
searchbar1.grid(row=0, column=1, padx=5, pady=5, sticky=W)
searchbutton1 = Button(frame1, text="Search", width=3, font="{Apple LiGothic} 9",
                       command=lambda: display_search(library, searchbar1.get(), thru_button1, buttonArr1, subframe1))
searchbutton1.grid(row=0, column=2, padx=5, pady=5)

# play button
ppbutton1 = Button(frame1, image=playpause, bg="black",
                   command=lambda: playorpause())
ppbutton1.place(x=175, y=325)

# subframe

subframe1 = Frame(frame1, width=300, height=250, bg="#0D0D0D")
subframe1.grid(row=2, column=1, padx=5, pady=5)

thru_button1 = Button(subframe1, image=thru_cover,
                      command=lambda: play_thread(library, "Through and Through"))
thru_button1.grid(row=0, column=0, padx=5, pady=5)

############################################

# frame2

frame2 = LabelFrame(stream, width=725, height=400, text="User 2", bg="black", fg="white")
frame2.grid(row=0, column=1, sticky=E)
frame2.grid_propagate(0)

# teamusic logo
logolabel2 = Label(frame2, image=logo, bg="black")
logolabel2.grid(row=0, column=0, padx=5, pady=5)
label2=Label(frame2, text="teamusic", bg="black",
             font = "{Apple LiGothic} 6 bold", fg="white")
label2.grid(row=1, column=0, padx=5, pady=5)

# Welcome, Thomas
welcome2 = Label(frame2, text="Welcome, Thomas", bg="black", fg="white", font="{Apple LiGothic} 9 bold")
welcome2.grid(row=1, column=1, padx=5, pady=5, sticky=W)

# search bar and button
searchbar2 = Entry(frame2, width=35, bg="white", font="{Apple LiGothic} 9")
searchbar2.grid(row=0, column=1, padx=5, pady=5, sticky=W)
searchbutton2 = Button(frame2, text="Search", width=3, font="{Apple LiGothic} 9",
                       command=lambda: display_search(library, searchbar2.get(), thru_button2, buttonArr2, subframe2))
searchbutton2.grid(row=0, column=2, padx=5, pady=5)

# play button
ppbutton2 = Button(frame2, image=playpause, bg="black",
                   command=lambda: playorpause())
ppbutton2.place(x=175, y=325)

# subframe2
subframe2 = Frame(frame2, width=300, height=250, bg="#0D0D0D")
subframe2.grid(row=2, column=1, padx=5, pady=5)

thru_button2 = Button(subframe2, image=thru_cover,
                      command=lambda: play_thread(library, "Through and Through"))
thru_button2.grid(row=0, column=0, padx=5, pady=5)

############################################

# frame 3

frame3 = LabelFrame(stream, width=725, height=512, text="User 3", bg="black", fg="white")
frame3.grid(row=1, column=0, sticky=W)
frame3.grid_propagate(0)

# teamusic logo
logolabel3 = Label(frame3, image=logo, bg="black")
logolabel3.grid(row=0, column=0, padx=5, pady=5)
label3=Label(frame3, text="teamusic", bg="black",
             font = "{Apple LiGothic} 6 bold", fg="white")
label3.grid(row=1, column=0, padx=5, pady=5)

# Welcome, Thomas
welcome3 = Label(frame3, text="Welcome, Thomas", bg="black", fg="white", font="{Apple LiGothic} 9 bold")
welcome3.grid(row=1, column=1, padx=5, pady=5, sticky=W)

# search bar and button
searchbar3 = Entry(frame3, width=35, bg="white", font="{Apple LiGothic} 9")
searchbar3.grid(row=0, column=1, padx=5, pady=5, sticky=W)
searchbutton3 = Button(frame3, text="Search", width=3, font="{Apple LiGothic} 9",
                       command=lambda: display_search(library, searchbar3.get(), thru_button3, buttonArr3, subframe3))
searchbutton3.grid(row=0, column=2, padx=5, pady=5)

# play button
ppbutton3 = Button(frame3, image=playpause, bg="black",
                   command=lambda: playorpause())
ppbutton3.place(x=175, y=325)

# subframe

subframe3 = Frame(frame3, width=300, height=250, bg="#0D0D0D")
subframe3.grid(row=2, column=1, padx=5, pady=5)

thru_button3 = Button(subframe3, image=thru_cover,
                      command=lambda: play_thread(library, "Through and Through"))
thru_button3.grid(row=0, column=0, padx=5, pady=5)

############################################

# frame 4

frame4 = LabelFrame(stream, width=725, height=512, text="User 4", bg="black", fg="white")
frame4.grid(row=1, column=1, sticky=E)
frame4.grid_propagate(0)

# teamusic logo
logolabel4 = Label(frame4, image=logo, bg="black")
logolabel4.grid(row=0, column=0, padx=5, pady=5)
label4=Label(frame4, text="teamusic", bg="black",
             font = "{Apple LiGothic} 6 bold", fg="white")
label4.grid(row=1, column=0, padx=5, pady=5)

# Welcome, Thomas
welcome4 = Label(frame4, text="Welcome, Thomas", bg="black", fg="white", font="{Apple LiGothic} 9 bold")
welcome4.grid(row=1, column=1, padx=5, pady=5, sticky=W)

# search bar and button
searchbar4 = Entry(frame4, width=35, bg="white", font="{Apple LiGothic} 9")
searchbar4.grid(row=0, column=1, padx=5, pady=5, sticky=W)
searchbutton4 = Button(frame4, text="Search", width=3, font="{Apple LiGothic} 9",
                       command=lambda: display_search(library, searchbar4.get(), thru_button4, buttonArr4, subframe4))
searchbutton4.grid(row=0, column=2, padx=5, pady=5)

# play button
ppbutton4 = Button(frame4, image=playpause, bg="black",
                   command=lambda: playorpause())
ppbutton4.place(x=175, y=325)

# subframe

subframe4 = Frame(frame4, width=300, height=250, bg="#0D0D0D")
subframe4.grid(row=2, column=1, padx=5, pady=5)

thru_button4 = Button(subframe4, image=thru_cover,
                      command=lambda: play_thread(library, "Through and Through"))
thru_button4.grid(row=0, column=0, padx=5, pady=5)

############################################
#test

stream.mainloop()