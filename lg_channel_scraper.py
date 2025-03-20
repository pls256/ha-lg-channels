import requests
from bs4 import BeautifulSoup
import json
import os

# Function to scrape the webpage and extract data
def scrape_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    categories = soup.find_all('h5')  # Assuming each table has a preceding h5 tag for its category
    data = []

    for category in categories:
        category_name = category.text.strip()  # Extract the category name

        # Skip rows where the category is null
        if not category_name:
            continue

        table = category.find_next('table')  # Find the table immediately after the category header

        if table:
            rows = table.find_all('tr')
            for row in rows:
                # Extracting Brand, Channel No, Channel Name, and Description
                brand_img = row.find('td', class_='brand __border-top')
                channel_no = row.find('td', class_='channel-no __border-top')
                channel_name = row.find('td', class_='channel-name __border-top')
                description = row.find('td', class_='description __border-top')

                # Exclude rows without an image
                if brand_img and brand_img.find('img') and channel_no and channel_name and description:
                    brand = brand_img.find('img')['src'] if brand_img.find('img') else "N/A"
                    channel_no_text = channel_no.text.strip()
                    channel_name = channel_name.text.strip()
                    description = description.text.strip()

                    # Extract the numeric part of "Channel No" by removing the "IP-" prefix
                    channel = channel_no_text.replace("IP-", "")

                    data.append({
                        "Category": category_name,
                        "Brand Image URL": brand,
                        "Channel": channel,
                        "Channel No": channel_no_text,
                        "Channel Name": channel_name,
                        "Description": description,
                    })

    return data

# Function to download images
def download_images(data, image_directory):
    if not os.path.exists(image_directory):
        os.makedirs(image_directory)  # Create the directory if it doesn't exist

    for item in data:
        image_url = "https://tv-experience.lg.com.au" + item["Brand Image URL"]  # Base URL + relative path
        image_name = os.path.join(image_directory, image_url.split("/")[-1])  # Extract the image file name

        try:
            # Send a GET request to download the image
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                with open(image_name, "wb") as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"Downloaded: {image_name}")
            else:
                print(f"Failed to download: {image_url}")
        except Exception as e:
            print(f"Error downloading {image_url}: {e}")

# Main function
def main():
    # URL of the webpage to scrape
    url = "https://tv-experience.lg.com.au/lg-channels"

    # Updated directory to save downloaded images
    image_directory = r"images\lg-channels"

    # Scrape data from the webpage
    data = scrape_data(url)

    # Write the cleaned data to the updated JSON file
    with open("lg-channels.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print("Data has been written to lg-channels.json")

    # Download images
    download_images(data, image_directory)

# Run the program
if __name__ == "__main__":
    main()
