import requests
from bs4 import BeautifulSoup
import re
import logging
import pyfiglet

# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to display ASCII art
def display_ascii_art():
    ascii_art = pyfiglet.figlet_format("OSINT Blogger")
    print(ascii_art)
    print('Created by Kensdy')

def check_blogger(url):
    try:
        # Browser headers to simulate a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Make the request to the page with browser headers
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an error for HTTP status codes other than 200

        # Parse the HTML of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Search for the meta tag with content='blogger' and name='generator'
        blogger_tag = soup.find('meta', {'content': 'blogger', 'name': 'generator'})

        # Check if the tag was found
        if blogger_tag:
            return True  # It is a Blogger site
        else:
            return False  # It is not a Blogger site

    except requests.exceptions.RequestException as e:
        logger.error(f"Error making request to {url}: {e}")
        return None  # Returns None in case of error

def find_blogger_owner(url):
    try:
        # Check if the site is made on Blogger
        if not check_blogger(url):
            print("The site is not made on Blogger.")
            return

        # Get the HTML content of the page
        response = requests.get(url)
        html_content = response.content.decode('utf-8')

        # Search for all occurrences of "blogger.com/profile/" followed by numbers
        profile_links = set(re.findall(r'blogger\.com/profile/(\d+)', html_content))

        # Create complete URLs for each found number
        complete_urls = [f"https://www.blogger.com/profile/{profile}" for profile in profile_links]

        # Show the results
        print("Found profiles:")
        for url in complete_urls:
            print(url)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error making request to {url}: {e}")

def identify_public_blogs(url):
    try:
        # Check if the link is from a profile on Blogger
        if 'blogger.com/profile/' not in url:
            print("The provided link is not from a Blogger profile.")
            return

        # Get the HTML content of the page
        response = requests.get(url)
        html_content = response.content

        # Check if the text "Profile Not Available" is present anywhere on the page
        if '<title>Profile Not Available</title>' in html_content.decode() or '<h1>Profile Not Available</h1>' in html_content.decode():
            print("The Blogger Profile you requested cannot be displayed. Various Blogger users have not yet opted to publicly share their profiles.")
        else:
            # Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find the desired elements
            sidebar_items = soup.find_all('li', class_='sidebar-item')

            # Iterate over the elements and extract information
            for item in sidebar_items:
                link = item.find('a')['href']
                name = item.find('a').text
                print(f"Name: {name}, Link: {link}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error making request to {url}: {e}")

# Display ASCII art at the beginning of the script
display_ascii_art()

# Main loop
while True:
    # Menu of choices
    print("\nChoose the tool by its numbers:")
    print("1- Check if a site was created using Blogger")
    print("2- Identify the owner's profile of a blog on Blogger")
    print("3- Identify public blogs associated with a profile on Blogger")
    print("4- Stop the script")

    option = input("Enter the number of the desired tool: ")

    if option == '1':
        site_url = input("Enter the URL of the site: ")
        result = check_blogger(site_url)

        if result is not None:
            if result:
                print("The site is made on Blogger.")
            else:
                print("The site is not made on Blogger.")

    elif option == '2':
        blog_url = input("Enter the URL of the blog: ")
        find_blogger_owner(blog_url)

    elif option == '3':
        profile_url = input("Enter the URL of the profile on Blogger: ")
        identify_public_blogs(profile_url)

    elif option == '4':
        print("Script terminated.")
        break

    else:
        print("Invalid option.")
