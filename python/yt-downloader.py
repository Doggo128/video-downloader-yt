from logging import DEBUG
from tkinter import *
import tkinter
from tkinter.font import Font
from typing import List
from pytube import YouTube

from tkinter import ttk
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename


DEBUG_VERSION = "v0.0"
DEBUG_PRINTERRORS = True
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 530
WINDOW_STARTX = 200
WINDOW_STARTY = 200

window = Tk() 
window.title("Youtube Downloader " + DEBUG_VERSION)

window.geometry( str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT) + "+" + str(WINDOW_STARTX) + "+" + str(WINDOW_STARTY) ) #Window dimensions (width x height + x + y)
window.resizable( width=False, height=False ) #This disables resizing the window

#filters user input for the youtube link formatting
def filterInput(str=""):
    #If string is empty
    if len(str) <= 0:
        return None
    

    #TODO: add checks for the youtube short urls (youtu.be links)
    if "youtube.com" not in str.lower():
        if DEBUG_PRINTERRORS == True:
            print( "youtube.com not in str" )
        return None
   
    return str



lblTitle = Label(window, text="Enter Link", font="Calibri")

lblVersion = Label(window, text=DEBUG_VERSION, font="Calibri")

inputBoxUrl = Entry( window, width=64)




lblFrameItag = LabelFrame(window, text="Streams", width=500, height=250)



treeITag = ttk.Treeview(lblFrameItag, height=8)
treeITag['columns'] = ( 'itag', 'type', 'vcodec', 'acodec', 'resolution', 'fps')

treeITag.column( '#0', width=0, anchor=CENTER, stretch=NO)
treeITag.column( 'itag', width=50, anchor=CENTER )
treeITag.column( 'type', width=80, anchor=CENTER)
treeITag.column( 'vcodec', width=80, anchor=CENTER)
treeITag.column( 'acodec', width=80, anchor=CENTER)
treeITag.column( 'resolution', width=100, anchor=CENTER)
treeITag.column( 'fps', width=50, anchor=CENTER)


treeITag.heading( '#0', text='', anchor=CENTER)
treeITag.heading( 'itag', text='ITag', anchor=CENTER)
treeITag.heading( 'type', text='Type', anchor=CENTER)
treeITag.heading( 'vcodec', text='V-Codec', anchor=CENTER)
treeITag.heading( 'acodec', text='A-Codec', anchor=CENTER)
treeITag.heading( 'resolution', text='Resolution', anchor=CENTER)
treeITag.heading( 'fps', text='FPS', anchor=CENTER)


lblFrame = LabelFrame(window, text="Video Information", width=400, height=150)

lblVidName = Label( lblFrame, text="Title: ", font="Calibri")
lblVidViews = Label( lblFrame, text="Views:", font="Calibri" )
lblVidDesc = Label( lblFrame, text="Description:\n", wraplength=300, justify="left", font="Calibri" )


lblHelp = Label(window, text="Help", fg="blue", cursor="hand2")

windowHelp = None


def clickedHelpMenu(self):
    #if window is already existing then exit
    windowHelp = Toplevel(window, width=256, height=400)
    windowHelp.title("Help")
    windowHelp.resizable( width=False, height=False )

    lblHeader1 = Label( windowHelp, text="Insert YouTube link @ 'Enter Link'.\nThen click the 'Fetch Video' button.\nOnce video details are grabbed, select your desired Stream.\nThen click the 'Download Stream' button. \nYou will be asked to pick a location to save the stream as a video file.", wraplength=200, justify="left", width=40, height=16)
    lblHeader1.place( x=0, y=0)

    lblHeader2 = Label( windowHelp, text="lorem ipsum", width=20, height=2)
    lblHeader1.place( x=10, y=5)

    return None

lblHelp.bind("<Button-1>", clickedHelpMenu)


selectedITag = 0

def itagSelected(self):
    curItem = treeITag.focus()
    print( treeITag.item(curItem) )
    x = list(treeITag.item(curItem).values() )
    

    global selectedITag
    selectedITag = x[2][0]

    #print( "Itag: %s" % x )
    if btnDownload["state"] == DISABLED:
        btnDownload["state"] = NORMAL

    return None


treeITag.bind('<ButtonRelease-1>', itagSelected)

#listBoxVidInfo = Listbox( window, width=15, height=5, selectmode="SINGLE", listvariable=StringVar())

global yt;




def fetchStreams():
    filteredLink = filterInput( inputBoxUrl.get() )

    global yt;
    yt = YouTube( filteredLink )

    yStream = yt.streams.filter()
    i = 0
    
    for stream in yStream:
        #itag id, type, vid codec, audio codec, resolution, fps
        treeITag.insert( parent='', index=i, iid=i, text='', values=( stream.itag, stream.type, stream.video_codec, stream.audio_codec, stream.resolution, stream.fps))
        i += 1
    


def getVideo():
    
    filteredLink = filterInput( inputBoxUrl.get() )

    if filteredLink is None:
        tkinter.messagebox.showerror( title="Invalid Link",  message="URL filter returned None")

        #lblTitle.configure(text="invalid link")
        return None
    global yt;
    yt = YouTube( filteredLink )


    #Title of video
    print("Title: ",yt.title)
    print("Views: ", yt.views )
    print( "Description: ",yt.description)

    lblVidName.config( text="Title: " + yt.title)
    lblVidViews.config( text="Views: " + str(yt.views) )
    lblVidDesc.config( text="Description:\n" + yt.description)

    #treeVD.insert( parent='', index=0, iid=0, text='', values=( yt.title, str(yt.views), yt.description) )

    fetchStreams()

        

#opens a file dialog and saves the youtube video
#TODO: Add selecting different streams to download
def downloadVideo():
    #If our youtube variable is empty we cannot download (fetch video info first)
    global yt;
    if yt is None:
        tkinter.messagebox.showerror( title="YouTube object is None",  message="No youtube data found (Make sure to fetch before downloading)")
        return None
    
    
    
    f = asksaveasfilename(initialfile = '', defaultextension=".mp4",filetypes=[("Video File","*.mp4"), ("All Files","*.*")])
    print("---------------------")
    #print("Chosen File Path: ", f)

    print( "Selected iTag: ", selectedITag)
    ys = yt.streams.get_by_itag(selectedITag)
    
    print("Downloading video...")
    #extract the output_path and filename from the selected SaveDialog
    #TODO: check if 'f' is empty or null
    raw = f.split('/')
    fileName = raw[len(raw)-1]
    
    filePath = ""
    for i in range( len(raw)-1):
        filePath = filePath + raw[i] + "/"
    
    print("File Path: ", filePath)
    print("File Name: ", fileName)
   
    ys.download( output_path=filePath, filename=fileName) 
    tkinter.messagebox.showerror( title="Complete!",  message="Video Download Finished")
    print("DONE")
    print("---------------------")



btnDownload = Button( lblFrameItag, text="Download Stream", width=16, height=1, command=downloadVideo, state=DISABLED)

btnGo = Button( window, text="Fetch Video", width=12, height=1, command=getVideo )


lblTitle.place( x=90, y=4 )


#width x height = 600 x 400 (urlbox is 64width)
inputBoxUrl.place( x=( 80  ), y=30 )
btnGo.place( x=480, y=30 )

#Video Information 
lblFrame.place( x=80, y=70 )
lblVidName.place( x=0, y=0)
lblVidViews.place( x=0, y=20)
lblVidDesc.place( x=0, y=40)



lblFrameItag.place( x=70, y=240)
treeITag.place( x=25, y=0) #x=80, y=250

btnDownload.place( x=300, y=195) #x=250, y=450
lblVersion.place( x=WINDOW_WIDTH - 40, y=WINDOW_HEIGHT - 30 )

lblHelp.place( x=WINDOW_WIDTH-80, y=WINDOW_HEIGHT - 30)


#print( type(widgets[0] ) )

#Button(window, text="create new window", command=None).pack()

    



#Number of views of video
#print("Number of views: ",yt.views)
#Description of video
#print("Description: ",yt.description)

#ys = yt.streams.get_by_itag('22')
#ys.download()


window.mainloop()