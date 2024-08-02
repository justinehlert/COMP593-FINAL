from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import apod_desktop
import ctypes
import os

# Initialize the image cache
apod_desktop.init_apod_cache()
script_dir = os.path.dirname(os.path.abspath(__file__))
NASAIcon = os.path.join(script_dir, 'nasa_logo_icon_170926-288813334.png')
image_cache_dir = os.path.join(script_dir, 'images')

filesList = apod_desktop.get_all_apod_titles()

# TODO: Create the GUI
root = Tk()
root.geometry('600x400')
root.title('Astronomy Picture of the Day Viewer')

icon = PhotoImage(file=NASAIcon)
root.iconphoto(False, icon)

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

app_id = 'COMP593.APODViewer'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

def handle_img_sel(event):
    sel_img_index = cbox_images.current()
    img = ImageTk.PhotoImage(Image.open(os.path.join(image_cache_dir, filesList[sel_img_index])))
    icon['file'] = img
    return

frm_img = Canvas(root, relief='groove')
frm_img.grid(row=0,column=0, columnspan=2, sticky='ns')
frm_img.columnconfigure(0, weight=1)
frm_img.rowconfigure(0, weight=1)

frm_viewer = ttk.LabelFrame(root, text='View Cached Image')
frm_viewer.grid(row=2,column=0, sticky='sw')
frm_viewer.columnconfigure(0, weight=1)
frm_viewer.rowconfigure(3, weight=1)

frm_get = ttk.LabelFrame(root, text='Get More Images')
frm_get.grid(row=2,column=1, sticky='sw')
frm_get.columnconfigure(1, weight=1)
frm_get.rowconfigure(3, weight=1)

frm_img.create_image(0,0, anchor=NW, image=icon)
#apod_img = ttk.Label(frm_img, image=icon)
#apod_img.grid(row=0, column=0, padx=10,pady=10, sticky='nsew')

apod_expl = ttk.Label(frm_img, text='')
apod_expl.grid(row=1, column=0, padx=10,pady=10, sticky='ns')

view_images = ttk.Label(frm_viewer, text='Select Image: ')
view_images.grid(row=0,column=0, padx=(20,10), pady=(10,20), sticky='n')

cbox_images = ttk.Combobox(frm_viewer, values=filesList, state='readonly')
cbox_images.grid(row=0,column=1)
cbox_images.bind('<<ComboboxSelected>>', handle_img_sel)
cbox_images.set('Select an image to preview')

desktop_btn = ttk.Button(frm_viewer, text='Set Desktop Background')

get_images_get = ttk.Label(frm_get, text='Select Date: ')
get_images_get.grid(row=0,column=0, padx=(10,20), pady=(10,20), sticky='n')


root.mainloop()