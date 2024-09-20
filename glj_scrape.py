import requests
from bs4 import BeautifulSoup

# URL of the page to scrape
url = "https://www.cambridge.org/core/journals/german-law-journal/all-issues"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the links to journal issues
    issue_links = []
    
    # Loop through all 'a' tags with href that contains '/core/journals/german-law-journal/issue/'
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if '/core/journals/german-law-journal/issue/' in href:
            full_link = "https://www.cambridge.org" + href
            issue_links.append(full_link)

    # Print all the journal issue links
    for link in issue_links:
        print(link)

else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
