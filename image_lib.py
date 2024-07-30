'''
Library of useful functions for working with images.
'''
import requests
import ctypes

def main():
    # TODO: Add code to test the functions in this module
    imageData = download_image('https://apod.nasa.gov/apod/image/0202/m78_aao_big.jpg')
    imagePath = r'C:\test\image.png'
    save_image_file(imageData, imagePath)
    set_desktop_background_image(imagePath)
    return

def download_image(image_url):
    """Downloads an image from a specified URL.

    DOES NOT SAVE THE IMAGE FILE TO DISK.

    Args:
        image_url (str): URL of image

    Returns:
        bytes: Binary image data, if succcessful. None, if unsuccessful.
    """
    # TODO: Complete function body
    
    img = requests.get(image_url)

    if img:
        print("Downloading iamge from" + image_url + " ...success")    
    return img.content if img else None

def save_image_file(image_data, image_path):
    """Saves image data as a file on disk.
    
    DOES NOT DOWNLOAD THE IMAGE.

    Args:
        image_data (bytes): Binary image data
        image_path (str): Path to save image file

    Returns:
        bool: True, if succcessful. False, if unsuccessful
    """
    # TODO: Complete function body
    try:
        with open(image_path, 'wb') as file:
            file.write(image_data)
    except Exception as e:
        print(e)
        return False
    return True

def set_desktop_background_image(image_path):
    """Sets the desktop background image to a specific image.

    Args:
        image_path (str): Path of image file

    Returns:
        bytes: True, if succcessful. False, if unsuccessful        
    """
    # TODO: Complete function body
        # Define the SPI_SETDESKWALLPAPER constant
    SPI_SETDESKWALLPAPER = 20
    # Define the SPIF_UPDATEINIFILE and SPIF_SENDCHANGE flags
    SPIF_UPDATEINIFILE = 1
    SPIF_SENDCHANGE = 2

    try:
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)
    except Exception as err:
        print('Set Desktop Background Error: ' + err)
        return False

    return True

def scale_image(image_size, max_size=(800, 600)):
    """Calculates the dimensions of an image scaled to a maximum width
    and/or height while maintaining the aspect ratio  

    Args:
        image_size (tuple[int, int]): Original image size in pixels (width, height) 
        max_size (tuple[int, int], optional): Maximum image size in pixels (width, height). Defaults to (800, 600).

    Returns:
        tuple[int, int]: Scaled image size in pixels (width, height)
    """
    ## DO NOT CHANGE THIS FUNCTION ##
    # NOTE: This function is only needed to support the APOD viewer GUI
    resize_ratio = min(max_size[0] / image_size[0], max_size[1] / image_size[1])
    new_size = (int(image_size[0] * resize_ratio), int(image_size[1] * resize_ratio))
    return new_size

if __name__ == '__main__':
    main()