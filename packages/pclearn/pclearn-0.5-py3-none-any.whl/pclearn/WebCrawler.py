import urllib.request
from html.parser import HTMLParser

# Create a subclass of HTMLParser to handle the extraction of links
class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    self.links.append(attr[1])

def fetch_page(url):
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching page: {e}")
        return None

# Take URL input from the user
url = input("Enter the URL to crawl: ")

# Fetch the page content
page_content = fetch_page(url)
if page_content is None:
    print("Page doesn't have any content")
else:
    # Parse the HTML content to find all links
    parser = LinkParser()
    parser.feed(page_content)

    # Print out all the links found on the page
    print("Links found on the page:")
    for link in parser.links:
        print(link)
