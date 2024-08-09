'''
Library for interacting with NASA's Astronomy Picture of the Day API.
'''
import requests
from datetime import date

NASAApiUrl = 'https://api.nasa.gov/planetary/apod'
APIkey = 'QrB8aDPqGLjRIbCSojF51r16h7i4I3OeYSeirm4p'

def main():
    # TODO: Add code to test the functions in this module
    apod = get_apod_info('1995-06-01')

    apodURL = get_apod_image_url(apod)
    return

def get_apod_info(apod_date):
    """Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.

    Args:
        apod_date (date): APOD date (Can also be a string formatted as YYYY-MM-DD)

    Returns:
        dict: Dictionary of APOD info, if successful. None if unsuccessful
    """
    #Complete the function body
    # Hint: The APOD API uses query string parameters: https://requests.readthedocs.io/en/latest/user/quickstart/#passing-parameters-in-urls
    # Hint: Set the 'thumbs' parameter to True so the info returned for video APODs will include URL of the video thumbnail image 
    firstDate = date.fromisoformat('1995-06-16')
    if type(apod_date) is str:
        apodDate = date.fromisoformat(str(apod_date))
    else:
        apodDate = apod_date

    if apodDate < firstDate:
        print('Error: Date out of range, Too early')
        return None
        

    payload = {'api_key': APIkey, 'date': apod_date, 'thumbs': True}    
    try:
        r = requests.get(NASAApiUrl, params=payload)
        
    except Exception as e:
        print(f'Error Getting image{e}')
        quit()
    if r.ok:
        print(f"Getting {apod_date} APOD information from NASA... Success")
        return r.json()
    else:
        print(f"Getting {apod_date} APOD information from NASA... Failed")
        return None
    

def get_apod_image_url(apod_info_dict):
    """Gets the URL of the APOD image from the dictionary of APOD information.

    If the APOD is an image, gets the URL of the high definition image.
    If the APOD is a video, gets the URL of the video thumbnail.

    Args:
        apod_info_dict (dict): Dictionary of APOD info from API

    Returns:
        str: APOD image URL
    """
    # TODO: Complete the function body
    if apod_info_dict:
        if apod_info_dict['media_type'] == 'image':
            try:
                url = apod_info_dict['hdurl']
            except KeyError:
                url = apod_info_dict['url']
        else:
            url = apod_info_dict['thumbnail_url']
        print(f"APOD Title: {apod_info_dict['title']}")
        print(f"APOD URL: {url}")
        return url
    # Hint: The APOD info dictionary includes a key named 'media_type' that indicates whether the APOD is an image or video
    else:
        return None
    

if __name__ == '__main__':
    main()