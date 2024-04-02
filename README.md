# Wikipedia Page Search

## Prerequisites

- Python 3.x
- Beautiful Soup 4
- Requests library

## How to Run

1. Clone this repository to your local machine.
2. Ensure you have Python installed.
3. Install the required dependencies by running `pip install beautifulsoup4 requests`.
4. Run the script `wikipedia_page_search.py`.

## Example Usage

    python wikipedia_page_search.py
    Enter the target Wikipedia page: [Target Wikipedia Page]
    Enter the starting Wikipedia page link: [Starting Wikipedia Page]

## Efficiency and Complexity

- The search algorithm has a time complexity of O(N \* M), where N is the number of hops and M is the number of links on each page.

## Parallelizing

- The script utilizes parallelization to improve performance by using the ThreadPoolExecutor from the concurrent.futures module.
- Parallelization is employed when searching through multiple links simultaneously, reducing the overall search time.
- This approach allows for more efficient utilization of system resources, especially when dealing with a large number of links.

# Time

~2-3 hours spent on this project
