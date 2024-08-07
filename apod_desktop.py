""" 
COMP 593 - Final Project

Description: 
  Downloads NASA's Astronomy Picture of the Day (APOD) from a specified date
  and sets it as the desktop background image.

Usage:
  python apod_desktop.py [apod_date]

Parameters:
  apod_date = APOD date (format: YYYY-MM-DD)
"""
from datetime import date
import hashlib as hash
import os
import image_lib
from sys import argv
import apod_api
import requests
import sqlite3
import re

# Full paths of the image cache folder and database
# - The image cache directory is a subdirectory of the specified parent directory.
# - The image cache database is a sqlite database located in the image cache directory.
script_dir = os.path.dirname(os.path.abspath(__file__))
image_cache_dir = os.path.join(script_dir, 'images')
image_cache_db = os.path.join(image_cache_dir, 'image_cache.db')
NASAIcon = os.path.join(script_dir, 'nasa_logo_icon_170926-288813334.png')

def main():
    ## DO NOT CHANGE THIS FUNCTION ##
    # Get the APOD date from the command line
    apod_date = get_apod_date()    

    # Initialize the image cache
    init_apod_cache()

    # Add the APOD for the specified date to the cache
    apod_id = add_apod_to_cache(apod_date)

    # Get the information for the APOD from the DB
    apod_info = get_apod_info(apod_id)

    get_all_apod_titles()

    # Set the APOD as the desktop background image
    if apod_id != 0:
        image_lib.set_desktop_background_image(apod_info['file_path'])

def get_apod_date():
    """Gets the APOD date
     
    The APOD date is taken from the first command line parameter.
    Validates that the command line parameter specifies a valid APOD date.
    Prints an error message and exits script if the date is invalid.
    Uses today's date if no date is provided on the command line.

    Returns:
        date: APOD date
    """
    # TODO: Complete function body TEST
    try:
        inputDate = argv[1]
    except IndexError:
        inputDate = date.today() 
    # Hint: The following line of code shows how to convert and ISO-formatted date string to a date object
    try:
        apod_date = date.fromisoformat(str(inputDate))
    except Exception as e:
        print(f'Error: {e}')
        quit()
    if apod_date > date.today():
        print("Error: APOD date cannot be in the future")
        quit()
    return apod_date

def init_apod_cache():
    """Initializes the image cache by:
    - Creating the image cache directory if it does not already exist,
    - Creating the image cache database if it does not already exist.
    """
    #Create the image cache directory if it does not already exist
    print(f"Image cache directory: {image_cache_dir}")
    try:
        os.mkdir(image_cache_dir)
    except FileExistsError:
        print("Image cache dir already exists")
    # TODO: Create the DB if it does not already exist
    print(f'Image cache DB: ' + image_cache_db)
    if not os.path.exists(image_cache_db):
        con = sqlite3.connect(image_cache_db)
        cur = con.cursor()

        create_tbl_query = """
        CREATE TABLE IF NOT EXISTS apod
        (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            info TEXT NOT NULL,
            filePath TEXT NOT NULL,
            sha256 TEXT NOT NULL
        );
        """
        cur.execute(create_tbl_query)

        con.commit()
        con.close()
    else:
        print("Image cache DB already exists.")

    return

def add_apod_to_cache(apod_date):
    """Adds the APOD image from a specified date to the image cache.
     
    The APOD information and image file is downloaded from the NASA API.
    If the APOD is not already in the DB, the image file is saved to the 
    image cache and the APOD information is added to the image cache DB.

    Args:
        apod_date (date): Date of the APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if a new APOD is added to the
        cache successfully or if the APOD already exists in the cache. Zero, if unsuccessful.
    """
    print("APOD date:", apod_date.isoformat())
    # TODO: Download the APOD information from the NASA API
    # Hint: Use a function from apod_api.py 
    apodInfo = apod_api.get_apod_info(apod_date)

    # TODO: Download the APOD image
    # Hint: Use a function from image_lib.py 
    imageURL = apod_api.get_apod_image_url(apodInfo)
    imgData = image_lib.download_image(imageURL)
    imgHash = hash.sha256(imgData).hexdigest()
    print("APOD SHA-256: " + imgHash)
    # TODO: Check whether the APOD already exists in the image cache
    # Hint: Use the get_apod_id_from_db() function below
    sqlID = get_apod_id_from_db(imgHash)
    if sqlID:
        print('APOD image is already in cache')
        return sqlID[0]

    # TODO: Save the APOD file to the image cache directory
    # Hint: Use the determine_apod_file_path() function below to determine the image file path
    # Hint: Use a function from image_lib.py to save the image file
    imgPath = determine_apod_file_path(apodInfo['title'], apod_api.get_apod_image_url(apodInfo))
    image_lib.save_image_file(imgData, imgPath)

    # TODO: Add the APOD information to the DB
    # Hint: Use the add_apod_to_db() function below
    imgID = add_apod_to_db(apodInfo['title'], apodInfo['explanation'], str(imgHash), imgPath)

    return imgID[0]

def add_apod_to_db(title, explanation, file_path, sha256):
    """Adds specified APOD information to the image cache DB.
     
    Args:
        title (str): Title of the APOD image
        explanation (str): Explanation of the APOD image
        file_path (str): Full path of the APOD image file
        sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: The ID of the newly inserted APOD record, if successful. Zero, if unsuccessful       
    """
    # TODO: Complete function body
    con = sqlite3.connect(image_cache_db)
    cur = con.cursor()

    add_image_query = """
        INSERT INTO apod
        (
        title,
        info,
        filePath,
        sha256
        )
        VALUES (?, ?, ?, ?);
        """
    newImage = (  
        title,
        explanation,
        sha256,
        file_path
    )
    try:
        cur.execute(add_image_query, newImage)
    except Exception as err:
        print('Add Image Query Error:' + err)
        return 0
    
    con.commit()

    cur.execute(f"SELECT id FROM apod")

    imageID = cur.fetchall()

    con.close()       
    return imageID[0]

def get_apod_id_from_db(image_sha256):
    """Gets the record ID of the APOD in the cache having a specified SHA-256 hash value
    
    This function can be used to determine whether a specific image exists in the cache.

    Args:
        image_sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if it exists. Zero, if it does not.
    """
    # TODO: Complete function body
    con = sqlite3.connect(image_cache_db)
    cur = con.cursor()

    imageQuery = f"""
        SELECT id FROM apod WHERE sha256 = '{image_sha256}'
    """

    try:
        cur.execute(imageQuery)
    except Exception as err:
        print(f'ID Query Error: {err}')
        return 0
    imageID = cur.fetchall()
    con.close()
    try:
        imageID = imageID[0]
    except:
        print('No file in database with this ID')
        list = []
        return list.append(0)
    return imageID[0]


def determine_apod_file_path(image_title, image_url):
    """Determines the path at which a newly downloaded APOD image must be 
    saved in the image cache. 
    
    The image file name is constructed as follows:
    - The file extension is taken from the image URL
    - The file name is taken from the image title, where:
        - Leading and trailing spaces are removed
        - Inner spaces are replaced with underscores
        - Characters other than letters, numbers, and underscores are removed

    For example, suppose:
    - The image cache directory path is 'C:\\temp\\APOD'
    - The image URL is 'https://apod.nasa.gov/apod/image/2205/NGC3521LRGBHaAPOD-20.jpg'
    - The image title is ' NGC #3521: Galaxy in a Bubble '

    The image path will be 'C:\\temp\\APOD\\NGC_3521_Galaxy_in_a_Bubble.jpg'

    Args:
        image_title (str): APOD title
        image_url (str): APOD image URL
    
    Returns:
        str: Full path at which the APOD image file must be saved in the image cache directory
    """
    # TODO: Complete function body
    # Hint: Use regex and/or str class methods to determine the filename.
    title = image_title.strip()
    title = re.sub(r'\s+', '_', title)
    title = re.sub(r'[\W]', '', title)

    pattern = r'\.([a-zA-Z0-9]+)$'

    match = re.search(pattern, image_url)

    imgExtension = '.' + match.group(1)

    imgPath = image_cache_dir + '\\' + title + imgExtension

    return imgPath

def get_apod_info(image_id):
    """Gets the title, explanation, and full path of the APOD having a specified
    ID from the DB.

    Args:
        image_id (int): ID of APOD in the DB

    Returns:
        dict: Dictionary of APOD information
    """
    # TODO: Query DB for image info
    con = sqlite3.connect(image_cache_db)
    cur = con.cursor()

    get_info_query = f"""
        SELECT title, info, filePath FROM apod WHERE id = '{image_id}'
    """
    try:
        cur.execute(get_info_query)
    except Exception as err:
        print(f'Get Info Query Error: {err}')
        
    infoQueryResult = cur.fetchall()
    # TODO: Put information into a dictionary
    apod_info = {
        'title': infoQueryResult[0][0], 
        'explanation': infoQueryResult[0][1],
        'file_path': infoQueryResult[0][2],
    }
    con.close()
    return apod_info

def get_all_apod_titles():
    """Gets a list of the titles of all APODs in the image cache

    Returns:
        list: Titles of all images in the cache
    """
    # TODO: Complete function body
    # NOTE: This function is only needed to support the APOD viewer GUI
    titles = []
    for file in os.listdir(image_cache_dir):
        full_path = os.path.join(image_cache_dir, file)
        if os.path.isfile(full_path) and not full_path.endswith('.db'):
            titles.append(file)
    return titles

if __name__ == '__main__':
    main()