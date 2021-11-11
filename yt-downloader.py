from tkinter import *
import tkinter
from typing import List
from pytube import YouTube

from tkinter import ttk
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename



window = Tk() 
window.title("Youtube Downloader v0")
window.geometry("600x500+500+500") #Window dimensions (width x height + x + y)
window.resizable( width=False, height=False ) #This disables resizing the window

#filters user input for the youtube link formatting
def filterInput(str=""):
    #If string is empty
    if len(str) <= 0:
        return None
   
    return str



lblTitle = Label(window, text="Enter Link")


inputBoxUrl = Entry( window, width=64)
#inputBoxUrl.place( x=100, y=100)

lblStreams = Label(window, text='Streams')


#The TreeView that displays the video data
treeVD = ttk.Treeview(window, height=2)
treeVD['columns']=('Title', 'Views', 'Description')

treeVD.column( '#0', width=0, anchor=CENTER, stretch=NO)
treeVD.column('Title',  width=80, anchor='w')
treeVD.column('Views',  width=80, anchor='w')
treeVD.column('Description', width=250, anchor='w')

treeVD.heading( '#0', text='', anchor=CENTER)
treeVD.heading( 'Title', text='Title', anchor=CENTER)
treeVD.heading( 'Views', text='Views', anchor=CENTER)
treeVD.heading( 'Description', text='Description', anchor=CENTER)




treeITag = ttk.Treeview(window, height=8)
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



selectedITag = 0

def itagSelected(self):
    curItem = treeITag.focus()
    print( treeITag.item(curItem) )
    x = list(treeITag.item(curItem).values() )
    #print( x[2][0] )
    

    #print( "ITag: ", x[2][0] )
    #print( "Type: ", x[2][1] )
    #print( "vcodec: %s", x[2][2] )

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

    treeVD.insert( parent='', index=0, iid=0, text='', values=( yt.title, str(yt.views), yt.description) )

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
    print("DONE")
    print("---------------------")



btnDownload = Button( window, text="Download Stream", width=16, height=1, command=downloadVideo, state=DISABLED)

btnGo = Button( window, text="Fetch Video", width=12, height=1, command=getVideo )


lblTitle.place( x=300, y=0 )


#width x height = 600 x 400 (urlbox is 64width)
inputBoxUrl.place( x=( 80  ), y=30 )
btnGo.place( x=480, y=30 )


treeVD.place( x=80, y=70)

lblStreams.place( x=300, y=180)
treeITag.place( x=80, y=200)

btnDownload.place( x=250, y=400)




#print( type(widgets[0] ) )

#Button(window, text="create new window", command=None).pack()

    



#Number of views of video
#print("Number of views: ",yt.views)
#Description of video
#print("Description: ",yt.description)

#ys = yt.streams.get_by_itag('22')
#ys.download()


window.mainloop()