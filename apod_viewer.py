from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkcalendar import *
from datetime import date
from datetime import datetime
import hashlib as hash
import apod_desktop
import ctypes
import os
import image_lib

# Initialize the image cache
apod_desktop.init_apod_cache()
script_dir = os.path.dirname(os.path.abspath(__file__))
NASAIcon = os.path.join(script_dir, 'nasa_logo_icon_170926-288813334.png')
image_cache_dir = os.path.join(script_dir, 'images')

filesList = apod_desktop.get_all_apod_titles()

# TODO: Create the GUI
root = Tk()
root.geometry('800x600')
root.title('Astronomy Picture of the Day Viewer')

image = Image.open(NASAIcon)
icon = ImageTk.PhotoImage(image)
root.iconphoto(False, icon)
img = ImageTk.PhotoImage(image)

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

app_id = 'COMP593.APODViewer'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

def file_hash(file_path):
    ''' Hashes a file based on a file's path

    Args:
        file_path (str): a files path to be hashed
    returns:
        Hash object : hashed file
    
    '''

    sha256 = hash.sha256()

    with open(file_path, "rb") as f:
        while True:
            data = f.read(65536) # arbitrary number to reduce RAM usage
            if not data:
                break
            sha256.update(data)

    return sha256.hexdigest()

def handle_img_sel(event):
    try:
        global img
        sel_img_index = cbox_images.current()
        path = os.path.join(image_cache_dir, filesList[sel_img_index])
        image = Image.open(path)
        image = image.resize((600, 400))
        img = ImageTk.PhotoImage(image)        
        apod_img.config(image=img)
        ihash = file_hash(path)
        print(f'APOD HASH: {ihash}')
        apodID = apod_desktop.get_apod_id_from_db(str(ihash))
        if apodID:
            print('ID Match')
            apodInfo = apod_desktop.get_apod_info(apodID)
            apod_expl['text'] = apodInfo['explanation']
        else:
            print('Error: No image with that ID')
            
    except Exception as e:
        print(f'Error handling image {e}')    
    return

def set_desktop_button():
    sel_pkm_index = cbox_images.current()
    icon = os.path.join(image_cache_dir, filesList[sel_pkm_index])
    image_lib.set_desktop_background_image(image_path=icon)
    return

def download_image():
    global filesList
    selected_date = date_entry.get_date()
    apod_desktop.add_apod_to_cache(selected_date)
    filesList = apod_desktop.get_all_apod_titles()
    return

frm_img = Frame(root, relief='groove')
frm_img.grid(row=0,column=0, columnspan=2, sticky='nsew')
frm_img.columnconfigure(0, weight=1)
frm_img.rowconfigure(0, weight=1)
frm_img.grid_propagate(False)

frm_expl = Frame(root, relief='groove')
frm_expl.grid(row=1,column=0, columnspan=2, sticky='ns')
frm_expl.columnconfigure(0, weight=1)
frm_expl.rowconfigure(0, weight=1)

frm_viewer = ttk.LabelFrame(root, text='View Cached Image')
frm_viewer.grid(row=2,column=0, sticky='sw')
frm_viewer.columnconfigure(0, weight=1)
frm_viewer.rowconfigure(3, weight=1)

frm_get = ttk.LabelFrame(root, text='Get More Images')
frm_get.grid(row=2,column=1, sticky='sw')
frm_get.columnconfigure(1, weight=1)
frm_get.rowconfigure(3, weight=1)

apod_img = ttk.Label(frm_img, image=icon)
apod_img.grid(row=0, column=0, padx=10,pady=10, sticky='ns')

apod_img.image = img

apod_expl = ttk.Label(frm_expl, text='', wraplength=600)
apod_expl.grid(row=0, column=0, padx=(20,10), pady=(10,20), sticky='nsew')


view_images = ttk.Label(frm_viewer, text='Select Image: ')
view_images.grid(row=0,column=0, padx=(20,10), pady=(10,20), sticky='n')

cbox_images = ttk.Combobox(frm_viewer, values=filesList, state='readonly')
cbox_images.grid(row=0,column=1)
cbox_images.bind('<<ComboboxSelected>>', handle_img_sel)
cbox_images.set('Select an image to preview')

desktop_btn = ttk.Button(frm_viewer, text='Set Desktop Background', command=set_desktop_button)
desktop_btn.grid(row=0,column=2)

get_images_get = ttk.Label(frm_get, text='Select Date: ')
get_images_get.grid(row=0,column=0, padx=(10,20), pady=(10,20), sticky='n')

date_entry = DateEntry(frm_get, 
                       width=14, 
                       background='lightblue', 
                       foreground='black', 
                       borderwidth=3,
                       date_pattern='y-mm-dd',
                       mindate=datetime.strptime('1995-05-01', '%Y-%m-%d'),
                       maxdate=date.today())
date_entry.grid(row=0, column=1, padx=10, pady=10)

get_images_button = ttk.Button(frm_get, text='Download Image', command=download_image)
get_images_button.grid(row=0,column=2)


root.mainloop()