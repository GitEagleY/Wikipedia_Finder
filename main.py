import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin

MAX_HOPS = 6

def get_links_from_page(url):
    try:
        # Send a GET request to the provided URL
        response = requests.get(url)
        # Raise an HTTPError if the response status code is not successful
        response.raise_for_status()
        # Parse the HTML content of the response using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find all <a> tags with the 'href' attribute present
        all_links = soup.find_all('a', href=True)
        # Filter links starting with "/wiki/"
        filtered_links = []  # Initialize an empty list to store filtered links
        for link in all_links:  # Iterate over each link in the list of all links
            if link['href'].startswith("/wiki/"):  # Check if the link starts with "/wiki/"
                filtered_links.append(link)  # If it does, add the link to the filtered list
        # Create absolute URLs by joining with base URL
        absolute_links = []  # Initialize an empty list to store absolute URLs
        for link in filtered_links:  # Iterate over each filtered link
            absolute_url = urljoin(url, link['href'])  # Join the base URL with the relative URL to create an absolute URL
            absolute_links.append(absolute_url)  # Add the absolute URL to the list

        return absolute_links
    except Exception as e:
        print(f"Error getting links from {url}: {e}")
        return []


def search_target_page(start_url, target_page):
    hop_buffer = {start_url: MAX_HOPS}  # Temporary buffer to store links and their hop counts
    visited = set()
    
    while hop_buffer:
        next_hop_buffer = {}  # Buffer for next hop
        
        # Iterate through each link and its remaining hops in the current buffer
        for link, hops_left in hop_buffer.items():
            # Mark the current link as visited
            visited.add(link)
            
            print(f"Hops left for {link}: {hops_left}")
           
            if hops_left == 0:
                continue  # Skip if hops left is 0

            # Get the links from the current page
            links = get_links_from_page(link)
            
            # Check if the target page is found in the links
            if target_page in links:
                print(f"Found target page {target_page}!")
                return [link, target_page]

            # Add new links to the next hop buffer if they have not been visited yet
            for next_link in links:
                if next_link not in visited:
                    next_hop_buffer[next_link] = hops_left - 1


    print("Target Wikipedia page not found within 6 hops.")
    return None

if __name__ == "__main__":
    target_page = input("Enter the target Wikipedia page: ")
    start_url = input("Enter the starting Wikipedia page link: ")
    path = search_target_page(start_url, target_page)
    if path:
        print("Page found:")
        print(" -> ".join(path))
