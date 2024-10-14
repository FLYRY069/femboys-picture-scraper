import requests
from bs4 import BeautifulSoup
import os
import random
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import utils
from utils import Logger

logger = Logger()

def read_proxies(file_path):
    try:
        with open(file_path, 'r') as file:
            proxies = file.read().splitlines()
        return proxies
    except FileNotFoundError:
        logger.err("Proxies file not found")
        return []

def fetch_page(url, proxies, use_proxy):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        if use_proxy and proxies:
            proxy = {'http': random.choice(proxies), 'https': random.choice(proxies)}
            response = requests.get(url, headers=headers, proxies=proxy)
        else:
            response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        logger.err(f"Failed to fetch page: {e}")
        return None

def sanitize_filename(filename):
    
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def download_image(img_url, save_dir, proxies, use_proxy):
    img_data = fetch_page(img_url, proxies, use_proxy)
    if img_data:
        img_name = os.path.join(save_dir, sanitize_filename(os.path.basename(img_url.split('?')[0])))
        try:
            with open(img_name, 'wb') as img_file:
                img_file.write(img_data)
            logger.inf(f"Downloaded {img_url}")
        except Exception as e:
            logger.err(f"Failed to save {img_url}: {e}")

def is_valid_image(img_url):
    
    unwanted_keywords = ['merch', 'gaming', 'adult', 'doll', 'gifs']
    return not any(keyword in img_url for keyword in unwanted_keywords)

def download_images(url, save_dir, proxies, use_proxy, img_count, thread_count):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    total_downloaded = 0
    pid = 0

    while total_downloaded < img_count:
        page_url = f"{url}&pid={pid}"
        page_content = fetch_page(page_url, proxies, use_proxy)
        if not page_content:
            break

        soup = BeautifulSoup(page_content, 'html.parser')
        img_tags = soup.find_all('img')

        img_urls = [img['src'] for img in img_tags if 'src' in img.attrs and img['src'].startswith('http') and is_valid_image(img['src'])]
        img_urls = img_urls[:img_count - total_downloaded]

        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = [executor.submit(download_image, img_url, save_dir, proxies, use_proxy) for img_url in img_urls]
            for future in as_completed(futures):
                future.result()

        total_downloaded += len(img_urls)
        logger.inf(f"Downloaded {len(img_urls)} images from {page_url}. Total downloaded: {total_downloaded}")

        pid += 42  # Move to the next page

# Example usage
URLs = [
    "https://rule34.xxx/index.php?page=post&s=list&tags=astolfo_%28fate%2fapocrypha%29+",
    "https://rule34.xxx/index.php?page=post&s=list&tags=oiled",
    "https://rule34.xxx/index.php?page=post&s=list&tags=sakurajima_mai+"
]
save_dir = "downloaded_images"
proxies_file = "data/proxies.txt"

while True:
    choice = logger.inp("MADE BY FLYRY : Enter '1' to load proxies from data/proxies.txt or '2' to not use proxies: ").strip()
    if choice == "1":
        proxies = read_proxies(proxies_file)
        use_proxy = True
        break
    elif choice == "2":
        proxies = []
        use_proxy = False
        break
    else:
        logger.err("Invalid choice. Please enter '1' or '2'.")

img_count = logger.inp("MADE BY FLYRY | HOW MUCH?: ", integer=True)
thread_count = logger.inp("MADE BY FLYRY | ENTER THE TRHEADS NUMBER : ", integer=True)

for url in URLs:
    download_images(url, save_dir, proxies, use_proxy, img_count, thread_count)