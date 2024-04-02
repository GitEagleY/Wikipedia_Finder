import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin

MAX_HOPS = 6

def get_links_from_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        all_links = soup.find_all('a', href=True)
        filtered_links = [urljoin(url, link['href']) for link in all_links if link['href'].startswith("/wiki/")]
        return filtered_links
    except Exception as e:
        print(f"Error getting links from {url}: {e}")
        return []

def search_target_page(start_url, target_page):
    hop_buffer = {start_url: MAX_HOPS}  # Temporary buffer to store links and their hop counts
    visited = set()
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        while hop_buffer:
            next_hop_buffer = {}  # Buffer for next hop
            
            # Submit tasks to executor for each link in the current hop buffer
            futures = {executor.submit(get_links_from_page, link): link for link, hops_left in hop_buffer.items()}

            # Process completed tasks
            for future in futures:
                link = futures[future]
                hops_left = hop_buffer[link]
                visited.add(link)
                print(f"Hops left for {link}: {hops_left}")

                try:
                    links = future.result()  # Get result of the task (list of links)
                    if target_page in links:
                        print(f"Found target page {target_page}!")
                        executor.shutdown(wait=False)
                        return [link, target_page]
                    for next_link in links:
                        if next_link not in visited:
                            next_hop_buffer[next_link] = hops_left - 1
                except Exception as e:
                    print(f"Error processing link {link}: {e}")

            hop_buffer = next_hop_buffer  # Update hop_buffer with new links

    print("Target Wikipedia page not found within 6 hops.")
    return None

if __name__ == "__main__":
    target_page = input("Enter the target Wikipedia page: ")
    start_url = input("Enter the starting Wikipedia page link: ")
    path = search_target_page(start_url, target_page)
    if path:
        print("Page found:")
        print(" -> ".join(path))
