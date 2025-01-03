import requests
from bs4 import BeautifulSoup
import os

def download_image(url, folder_path):
    # Get the image content
    response = requests.get(url)
    if response.status_code == 200:
        # Extract the image name from the URL
        image_name = url.split("/")[-1]
        # Save the image to the specified folder
        with open(os.path.join(folder_path, image_name), 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {image_name}")

def scrape_images(url, folder_path):
    # Get the content of the webpage
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all image tags
        img_tags = soup.find_all('img')
        
        # Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        for img in img_tags:
            img_url = img.get('src')
            # Check if the image URL is valid
            if img_url:
                # Complete the URL if it's relative
                if not img_url.startswith(('http://', 'https://')):
                    img_url = requests.compat.urljoin(url, img_url)
                download_image(img_url, folder_path)
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

# Example usage:
url = 'https://example.com'
folder_path = 'downloaded_images'
scrape_images(url, folder_path)
