import tkinter as tk
import threading
import pygame
from pygame import mixer
from tkinter import *
from PIL import Image, ImageTk


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


# loads all the songs into the pygame mixer tool
#def loadtomixer(playlist):
    #for song in playlist:
        #mixer.music.load(playlist[song])


# defines which song shall be chosen
def choose_song():
    return -1


# collects the text put into the search bar
def searchquery(playlist):
    entered_text = searchbar.get()

    for song in playlist:
        if entered_text in song:
            pq.push(song, 0)


def display_search(playlist, search, album_button, buttonArr,pq):
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
        lower_song= key.lower()
        if search in lower_song:
            buttonArr[0][i] = Button(stream, text=key, width=20,command=lambda song=key:play_thread(library, song), font="{Apple LiGothic} 18")
            buttonArr[0][i].grid(row=2 + i, column=1, padx=8, pady=10, sticky=W)
            buttonArr[1][i] = Button(stream, text="Play Next",command=lambda song=key:play_next(pq,song), width=10, font="{Apple LiGothic} 18")
            buttonArr[1][i].grid(row=2 + i, column=2, padx=8, pady=10, sticky=W)
            buttonArr[2][i] = Button(stream, text="Add to Queue",command=lambda song=key:add_to_queue(pq,song), width=15, font="{Apple LiGothic} 18")
            buttonArr[2][i].grid(row=2 + i, column=3, padx=8, pady=10, sticky=W)
        i = i + 1


def play(playlist, song_name):
    chosen_song = playlist[song_name]
    mixer.music.load(chosen_song)
    mixer.music.play()


def play_thread(library, song):
    t = threading.Thread(target=play, args=(library, song))
    t.start()


# difference is that this function simply plays or pauses the current song playing in queue instead of referencing
def playorpause():
    if pygame.mixer.music.get_busy():
        mixer.music.pause()
    else:
        mixer.music.unpause()


def play_next(pq,song):
    nextSong = PriorityQueueNode(song, 0)
    nextSong.next = pq.front
    pq.front = nextSong
    #currNode=pq.front
    #while(currNode!=None):
    #    currNode.priority+=1
    #    currNode=currNode.next
    #pq.push(song,0)
    print("\n\n\n")
    pq.traverse()


def add_to_queue(pq,song):
    if pq.front == None:
        newSong = PriorityQueueNode(song, 0)
        pq.front=newSong
    else:
        currNode = pq.front
        while(currNode.next != None):
            currNode = currNode.next
        currNode.next = newSong = PriorityQueueNode(song, currNode.priority)

    #max=0
    #currNode=pq.front
    #while(currNode!=None):
    #    if (currNode.priority>max):
    #        max=currNode.priority
    #    currNode = currNode.next
    #pq.push(song,max+1)
    print("\n\n\n")
    pq.traverse()


if __name__ == '__main__':
    # creating our hash table of songs
    library = {
        'Through and Through': 'thru.mp3',
        'Adore You': 'adoreyou.mp3',
        'Love Me Back': 'lovemeback.mp3'
    }

    #createqueue(library)
    pq = PriorityQueue()
    pq.push("thru.mp3", 1)
    pq.push("hi", 2)
    pq.push("wassup", 3)
    pq.push("yo", 0)
    pq.traverse()

    # using tkinter to create our GUI
    stream = Tk()
    stream.title("Teamusic")  # window title
    stream.geometry("1450x1025")  # fixed window size
    stream.configure(background="black")  # aesthetic choice

    # Initializing pygame audio mixer
    mixer.init()

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
    searchbar = Entry(stream, width=45, bg="white", font="{Apple LiGothic} 18")
    searchbar.grid(row=0, column=1, padx=8, pady=50, sticky=W)

    # creating a button to initiate the search
    buttonArr = [[0 for x in range(3)] for x in range(len(library))]
    searchbutton = Button(stream, text="Search", command=lambda: display_search(library, searchbar.get(), thru_button, buttonArr,pq), width=6, font="{Apple LiGothic} 18")
    searchbutton.grid(row=0, column=2, padx=8, pady=50, sticky=W)

    # creating play and pause button
    playpause_orig = Image.open("playpause.png")
    resize_playpause = playpause_orig.resize((100, 75))
    playpause = ImageTk.PhotoImage(resize_playpause)
    ppbutton = Button(stream, image=playpause, command=lambda:playorpause(), width=100, font="{Apple LiGothic} 18")
    ppbutton.grid(row=5, column=1, padx=8, pady=10, sticky=W)

    # play button for songs
    # Khai Dreams Song
    thru_cover_orig = Image.open("thru.png")
    resize_thru_cover = thru_cover_orig.resize((500, 300))
    thru_cover = ImageTk.PhotoImage(resize_thru_cover)
    # creating label for button event
    thru_label = Label(image=thru_cover)
    # button to play in library
    thru_button = Button(stream, image=thru_cover,
                         command=lambda: play_thread(library, "Through and Through"))
    thru_button.grid(row=2, column=1, padx=7, pady=100, sticky=W)
    #thru_button = Button(stream, image=thru_cover,
                         #command=lambda: play(library, "Through and Through")) \
        #.grid(row=2, column=1, padx=7, pady=100, sticky=W)

    stream.mainloop()

    print('\nPyChar')
    print('hi')
    print('hello !')



