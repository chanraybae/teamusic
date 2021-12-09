import tkinter as tk
import sys
import threading
import pygame
from pygame import mixer
from tkinter import *
from multiprocessing import Process
from PIL import Image, ImageTk

eventstart = 0
SONG_END = pygame.USEREVENT + 1


# Creating the Priority Queue class to use for linking songs in the queue
class PriorityQueueNode:

    def __init__(self, value, pr):
        self.data = value
        self.priority = pr
        self.next = None


# implementing the Priority Queue
class PriorityQueue:

    def __init__(self):

        self.front = None

    # Method to check Priority Queue is Empty
    # or not if Empty then it will return True
    # Otherwise False
    def isempty(self):

        return True if self.front == None else False

    # Method to add items in Priority Queue according to their priority value
    def push(self, value, priority):

        # Condition check for checking Priority Queue is empty or not
        if self.isempty():

            # Creating a new node and assigning it to class variable
            self.front = PriorityQueueNode(value, priority)

            # Returning 1 for successful execution
            return 1

        else:

            # Special condition check to see that first node priority value
            if self.front.priority > priority:

                # Creating a new node
                newnode = PriorityQueueNode(value, priority)

                # Updating the new node next value
                newnode.next = self.front

                # Assigning it to self.front
                self.front = newnode

                # Returning 1 for successful execution
                return 1

            else:

                # Traversing through Queue until it finds the next smaller priority node
                temp = self.front

                while temp.next:

                    # If same priority node found then current node will come after previous node
                    if priority <= temp.next.priority:
                        break

                    temp = temp.next

                newnode = PriorityQueueNode(value, priority)
                newnode.next = temp.next
                temp.next = newnode

                # Returning 1 for successful execution
                return 1

    # Method to remove high priority item from the Priority Queue
    def pop(self):
        # Checking if the queue is empty - if so returns nothing
        if self.isempty():
            return

        else:
            # Removing high priority node from Priority Queue, and updating front with next node
            self.front = self.front.next
            return 1

    # Method to return highest priority node value Not removing it
    def peek(self):

        # Checking if the queue is empty - if so returns nothing
        if self.isempty():
            return
        else:
            return self.front.data

    # Method to Traverse through Priority Queue
    def traverse(self):

        # Condition check for checking Priority Queue is empty or not
        if self.isempty():
            return "No songs currently queued."
        else:
            temp = self.front
            while temp:
                print(temp.data, end=" ")
                temp = temp.next


def display_search(playlist, search, album_button, buttonArr, pq, targ_frame):
    album_button.grid_remove()
    i = 0
    j=0
    for j in range(3):
        for i in range(len(playlist)):
            if (buttonArr[j][i]!=0):
                buttonArr[j][i].grid_remove()
            i = i + 1
        j=j+1
    i = 0
    search = search.lower()
    for key in playlist:
        lower_song = key.lower()
        if search in lower_song:
            buttonArr[0][i] = Button(targ_frame, text=key, width=30,command=lambda song=key:play_thread(library, song),
                                     font="{Apple LiGothic} 9", bg='#231f20', fg='white')
            buttonArr[0][i].grid(row=2 + i, column=1, padx=8, pady=10, sticky=W)
            buttonArr[1][i] = Button(targ_frame, text="Play Next",command=lambda song=key:play_next(pq, song, playlist), width=8, font="{Apple LiGothic} 9", bg='#231f20', fg='white')
            buttonArr[1][i].grid(row=2 + i, column=2, padx=8, pady=10, sticky=W)
            buttonArr[2][i] = Button(targ_frame, text="Add to Queue",command=lambda song=key:add_to_queue(pq, song, playlist), width=15, font="{Apple LiGothic} 9", bg='#231f20', fg='white')
            buttonArr[2][i].grid(row=2 + i, column=3, padx=8, pady=10, sticky=W)
        i = i + 1


def back_to_main(playlist, buttonArr, album_button):
    for j in range(3):
        for i in range(len(playlist)):
            if buttonArr[j][i] != 0:
                buttonArr[j][i].grid_remove()
    # puts logos back
    album_button.grid(row=0, column=0, padx=5, pady=5)

def play(playlist, song_name):
    chosen_song = playlist[song_name]
    mixer.music.load(chosen_song)
    mixer.music.play()


def play_thread(library, song):
    t = threading.Thread(target=play, args=(library, song))
    t.start()


def skip_song(library, pq):
    if(pq.front == None):
        return
    song = pq.front.data
    pq.pop()
    print("\n")
    pq.traverse()
    play_thread(library, song)


# difference is that this function simply plays or pauses the current song playing in queue instead of referencing
def playorpause():
    if pygame.mixer.music.get_busy():
        mixer.music.pause()
    else:
        mixer.music.unpause()


def play_next(pq,song, playlist):
    nextSong = PriorityQueueNode(song, 0)
    nextSong.next = pq.front
    pq.front = nextSong

    global eventstart
    eventstart += 1

    pygame.mixer.music.set_endevent(SONG_END)
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.queue(str(playlist[song]))
    else:
        mixer.music.load(str(playlist[song]))
        mixer.music.play()
        pq.pop()

    print("\n\n\n")
    print(eventstart)
    pq.traverse()


def add_to_queue(pq,song, playlist):
    global eventstart
    eventstart += 1

    pygame.mixer.music.set_endevent(SONG_END)

    if pq.front == None:
        newSong = PriorityQueueNode(song, 0)
        pq.front = newSong
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.queue(str(playlist[song]))
        else:
            mixer.music.load(str(playlist[song]))
            mixer.music.play()
            pq.pop()
    else:
        currNode = pq.front
        while(currNode.next is not None):
            currNode = currNode.next
        currNode.next = newSong = PriorityQueueNode(song, currNode.priority)
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.queue(str(playlist[song]))
        else:
            mixer.music.load(str(playlist[song]))
            mixer.music.play()
            pq.pop()

    print("\n\n\n")
    pq.traverse()


# detects if a song has ended and removes it from the Priority Queue (demonstrated when traversed)
def songend():
    var = True
    while var:
        global eventstart
        global SONG_END

        if eventstart > 0:
            for event in pygame.event.get():
                if event.type == SONG_END:
                    pq.pop()


if __name__ == '__main__':
    # creating our hash table of songs
    library = {
        'Bruh - Test': 'bruh.mp3',
        'Through and Through - Khai Dreams': 'thru.mp3',
        'Adore You - Harry Styles': 'adoreyou.mp3',
        'Love Me Back - Social House': 'lovemeback.mp3'
    }

    # creating an instance of the priority queue
    pq = PriorityQueue()

    # button array for search results
    # second for x in range refers to the number of buttons we have after search (3 buttons)
    buttonArr1 = [[0 for x in range(len(library))] for x in range(3)]
    buttonArr2 = [[0 for x in range(len(library))] for x in range(3)]
    buttonArr3 = [[0 for x in range(len(library))] for x in range(3)]
    buttonArr4 = [[0 for x in range(len(library))] for x in range(3)]

    ############################################

    # create the tkinter window and initialize the pygame audio mixer
    stream = Tk()
    stream.title("Teamusic Split View")  # window title
    stream.geometry("1450x1010")  # window dimensions
    stream.configure(background="black")

    mixer.init()
    pygame.init()
    t = threading.Thread(target=songend, args=())
    t.start()
    ############################################

    # preparing images for inclusion in GUI

    # setting up the teamusic image logo
    logo_orig = Image.open("logo.jpg")
    resize_logo = logo_orig.resize((50, 38))
    logo = ImageTk.PhotoImage(resize_logo)

    # setting up the play/pause button
    playpause_orig = Image.open("playpause.png")
    resize_playpause = playpause_orig.resize((25, 25))
    playpause = ImageTk.PhotoImage(resize_playpause)

    # setting up the skip button
    skipsong_orig = Image.open("skipsong.png")
    resize_skipsong = skipsong_orig.resize((25, 25))
    skipsong = ImageTk.PhotoImage(resize_skipsong)

    # Khai Dreams Through and Through
    thru_cover_orig = Image.open("thru.png")
    resize_thru_cover = thru_cover_orig.resize((250, 150))
    thru_cover = ImageTk.PhotoImage(resize_thru_cover)

    ############################################

    # frame 1

    frame1 = LabelFrame(stream, width=725, height=500, text="User 1", bg="black", fg="white")
    frame1.grid(row=0, column=0, sticky=W)
    frame1.grid_propagate(0)

    # teamusic logo
    logobutton1 = Button(frame1, image=logo, bg="black", borderwidth=0,
                         command=lambda: back_to_main(library, buttonArr1, thru_button1))
    logobutton1.grid(row=0, column=0, padx=15, pady=5)
    label1 = Label(frame1, text="teamusic", bg="black",
                   font="{Apple LiGothic} 6 bold", fg="white")
    label1.grid(row=1, column=0, padx=15, pady=5)

    # Welcome, Thomas
    welcome1 = Label(frame1, text="Welcome, Thomas", bg="black", fg="white", font="{Apple LiGothic} 9 bold")
    welcome1.grid(row=1, column=1, padx=5, pady=5, sticky=W)

    # search bar and button
    searchbar1 = Entry(frame1, width=60, bg="white", font="{Apple LiGothic} 9")
    searchbar1.grid(row=0, column=1, padx=10, pady=5, sticky=W)
    searchbutton1 = Button(frame1, text="Search", width=6, font="{Apple LiGothic} 9",
                           command=lambda: display_search(library, searchbar1.get(), thru_button1, buttonArr1, pq,
                                                          subframe1))
    searchbutton1.grid(row=0, column=2, padx=5, pady=5)

    # play button
    ppbutton1 = Button(frame1, image=playpause, bg="black",
                       command=lambda: playorpause(), bd = 0)
    ppbutton1.place(x=25, y=425)

    # skip button
    skipbutton1 = Button(frame1, image=skipsong, bg="black",
                       command=lambda: skip_song(library,pq), bd = 0)
    skipbutton1.place(x=25, y=375)

    theCanvas = Canvas(frame1,bg="white",width=100, height=50)
    queueRect=theCanvas.create_rectangle(50,0,100,50,fill='red')

    # subframe

    subframe1 = Frame(frame1, width=445, height=250, bg="black")
    subframe1.grid(row=2, column=1, padx=5, pady=5)
    subframe1.grid_propagate(0)

    thru_button1 = Button(subframe1, image=thru_cover,
                          command=lambda: play_thread(library, "Through and Through - Khai Dreams"))
    thru_button1.grid(row=0, column=0, padx=5, pady=5)

    ############################################

    # frame 2

    frame2 = LabelFrame(stream, width=725, height=500, text="User 2", bg="black", fg="white")
    frame2.grid(row=0, column=1, sticky=W)
    frame2.grid_propagate(0)

    # teamusic logo
    logobutton2 = Button(frame2, image=logo, bg="black", borderwidth=0,
                         command=lambda: back_to_main(library, buttonArr2, thru_button2))
    logobutton2.grid(row=0, column=0, padx=15, pady=5)
    label2 = Label(frame2, text="teamusic", bg="black",
                   font="{Apple LiGothic} 6 bold", fg="white")
    label2.grid(row=1, column=0, padx=15, pady=5)

    # Welcome, Thomas
    welcome2 = Label(frame2, text="Welcome, Ray", bg="black", fg="white", font="{Apple LiGothic} 9 bold")
    welcome2.grid(row=1, column=1, padx=5, pady=5, sticky=W)

    # search bar and button
    searchbar2 = Entry(frame2, width=60, bg="white", font="{Apple LiGothic} 9")
    searchbar2.grid(row=0, column=1, padx=10, pady=5, sticky=W)
    searchbutton2 = Button(frame2, text="Search", width=6, font="{Apple LiGothic} 9",
                           command=lambda: display_search(library, searchbar2.get(), thru_button2, buttonArr2, pq,
                                                          subframe2))
    searchbutton2.grid(row=0, column=2, padx=5, pady=5)

    # play button
    ppbutton2 = Button(frame2, image=playpause, bg="black",
                       command=lambda: playorpause(), bd = 0)
    ppbutton2.place(x=25, y=425)

    # skip button
    skipbutton2 = Button(frame2, image=skipsong, bg="black",
                       command=lambda: playorpause(), bd = 0)
    skipbutton2.place(x=25, y=375)

    # subframe

    subframe2 = Frame(frame2, width=445, height=250, bg="black")
    subframe2.grid(row=2, column=1, padx=5, pady=5)
    subframe2.grid_propagate(0)

    thru_button2 = Button(subframe2, image=thru_cover,
                          command=lambda: play_thread(library, "Through and Through - Khai Dreams"))
    thru_button2.grid(row=0, column=0, padx=5, pady=5)

    ############################################

    # frame 3

    frame3 = LabelFrame(stream, width=725, height=500, text="User 3", bg="black", fg="white")
    frame3.grid(row=1, column=0, sticky=W)
    frame3.grid_propagate(0)

    # teamusic logo
    logobutton3 = Button(frame3, image=logo, bg="black", borderwidth=0,
                         command=lambda: back_to_main(library, buttonArr3, thru_button3))
    logobutton3.grid(row=0, column=0, padx=15, pady=5)
    label3 = Label(frame3, text="teamusic", bg="black",
                   font="{Apple LiGothic} 6 bold", fg="white")
    label3.grid(row=1, column=0, padx=15, pady=5)

    # Welcome, Thomas
    welcome3 = Label(frame3, text="Welcome, Katie", bg="black", fg="white", font="{Apple LiGothic} 9 bold")
    welcome3.grid(row=1, column=1, padx=5, pady=5, sticky=W)

    # search bar and button
    searchbar3 = Entry(frame3, width=60, bg="white", font="{Apple LiGothic} 9")
    searchbar3.grid(row=0, column=1, padx=10, pady=5, sticky=W)
    searchbutton3 = Button(frame3, text="Search", width=6, font="{Apple LiGothic} 9",
                           command=lambda: display_search(library, searchbar3.get(), thru_button3, buttonArr3, pq,
                                                          subframe3))
    searchbutton3.grid(row=0, column=2, padx=5, pady=5)

    # play button
    ppbutton3 = Button(frame3, image=playpause, bg="black",
                       command=lambda: playorpause(), bd = 0)
    ppbutton3.place(x=25, y=425)

    # skip button
    skipbutton3 = Button(frame3, image=skipsong, bg="black",
                       command=lambda: playorpause(), bd = 0)
    skipbutton3.place(x=25, y=375)

    # subframe

    subframe3 = Frame(frame3, width=445, height=250, bg="black")
    subframe3.grid(row=2, column=1, padx=5, pady=5)
    subframe3.grid_propagate(0)

    thru_button3 = Button(subframe3, image=thru_cover,
                          command=lambda: play_thread(library, "Through and Through - Khai Dreams"))
    thru_button3.grid(row=0, column=0, padx=5, pady=5)

    ############################################

    # frame 4

    frame4 = LabelFrame(stream, width=725, height=500, text="User 4", bg="black", fg="white")
    frame4.grid(row=1, column=1, sticky=W)
    frame4.grid_propagate(0)

    # teamusic logo
    logobutton4 = Button(frame4, image=logo, bg="black", borderwidth=0,
                         command=lambda: back_to_main(library, buttonArr4, thru_button4))
    logobutton4.grid(row=0, column=0, padx=15, pady=5)
    label4 = Label(frame4, text="teamusic", bg="black",
                   font="{Apple LiGothic} 6 bold", fg="white")
    label4.grid(row=1, column=0, padx=15, pady=5)

    # Welcome, Thomas
    welcome4 = Label(frame4, text="Welcome, Rory", bg="black", fg="white", font="{Apple LiGothic} 9 bold")
    welcome4.grid(row=1, column=1, padx=5, pady=5, sticky=W)

    # search bar and button
    searchbar4 = Entry(frame4, width=60, bg="white", font="{Apple LiGothic} 9")
    searchbar4.grid(row=0, column=1, padx=10, pady=5, sticky=W)
    searchbutton4 = Button(frame4, text="Search", width=6, font="{Apple LiGothic} 9",
                           command=lambda: display_search(library, searchbar4.get(), thru_button4, buttonArr4, pq,
                                                          subframe4))
    searchbutton4.grid(row=0, column=2, padx=5, pady=5)

    # play button
    ppbutton4 = Button(frame4, image=playpause, bg="black",
                       command=lambda: playorpause(), bd = 0)
    ppbutton4.place(x=25, y=425)

    # skip button
    skipbutton4 = Button(frame4, image=skipsong, bg="black",
                       command=lambda: playorpause(), bd = 0)
    skipbutton4.place(x=25, y=375)

    # subframe

    subframe4 = Frame(frame4, width=445, height=250, bg="black")
    subframe4.grid(row=2, column=1, padx=5, pady=5)
    subframe4.grid_propagate(0)

    thru_button4 = Button(subframe4, image=thru_cover,
                          command=lambda: play_thread(library, "Through and Through - Khai Dreams"))
    thru_button4.grid(row=0, column=0, padx=5, pady=5)

    ############################################
    # test

    stream.mainloop()



