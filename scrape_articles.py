import requests
from bs4 import BeautifulSoup

# Base URL
base_url = "https://www.cambridge.org"

# URL of the page to scrape
url = "https://www.cambridge.org/core/journals/german-law-journal/all-issues"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the links to journal issues
    issue_data = []

    # Loop through all 'a' tags with href that contains '/core/journals/german-law-journal/issue/'
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if '/core/journals/german-law-journal/issue/' in href:
            # Extract additional information (Title, Issue, Date)
            title = a_tag.find('span', class_='issue').text if a_tag.find('span', class_='issue') else "No title available"
            date = a_tag.find('span', class_='date').text if a_tag.find('span', class_='date') else "No date available"
            
            full_link = base_url + href
            
            # Append all collected data for this issue to the issue_data list
            issue_data.append({
                'link': full_link,
                'title': title,
                'date': date
            })

    # Now, for each issue link, visit the page and extract the articles and their details
    for issue in issue_data:
        print(f"Journal Issue: {issue['title']} ({issue['date']})")
        print(f"Link: {issue['link']}")

        # Send a request to the journal issue page
        issue_response = requests.get(issue['link'])
        if issue_response.status_code == 200:
            issue_soup = BeautifulSoup(issue_response.content, 'html.parser')
            
            # Find all articles in the issue
            articles = issue_soup.find_all('div', class_='representation overview search')
            for article in articles:
                # Extract the article title and link
                title_tag = article.find('a', class_='part-link')
                article_title = title_tag.text.strip() if title_tag else "No title available"
                
                # If the article has a specific link, use it; otherwise, use the issue link
                article_link = base_url + title_tag['href'] if title_tag else issue['link']
                
                # Extract the author(s)
                author_tag = article.find('a', class_='more-by-this-author')
                author_name = author_tag.text.strip() if author_tag else "No author available"
                
                # Extract the publication date
                pub_date_tag = article.find('span', class_='date')
                pub_date = pub_date_tag.text.strip() if pub_date_tag else "No date available"
                
                # Extract volume and issue number
                volume_issue_tag = article.find('span', class_='volume')
                if volume_issue_tag:
                    volume_issue_text = volume_issue_tag.text.strip().split('-')
                    volume = volume_issue_text[0].strip() if len(volume_issue_text) > 0 else "No volume available"
                    issue = volume_issue_text[1].strip() if len(volume_issue_text) > 1 else "No issue available"
                else:
                    volume = "No volume available"
                    issue = "No issue available"
                
                # Print the extracted article details
                print(f"  Article Title: {article_title}")
                print(f"  Article Link: {article_link}")
                print(f"  Author(s): {author_name}")
                print(f"  Published Date: {pub_date}")
                print(f"  Volume: {volume}")
                print(f"  Issue: {issue}")
                
        print("\n")
    
    # Count the number of links
    print(f"Total number of journal issues: {len(issue_data)}")

else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
