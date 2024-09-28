import urllib.request
from html.parser import HTMLParser
class URLLinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.found_links = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attribute in attrs:
                if attribute[0] == 'href':
                    self.found_links.append(attribute[1])
def get_webpage_content(webpage_url):
    try:
        with urllib.request.urlopen(webpage_url) as response:
            return response.read().decode('utf-8')
    except Exception as error:
        print(f"Error fetching page: {error}")
        return None
webpage_url = input("Enter the URL to crawl: ")
content = get_webpage_content(webpage_url)
if content is None:
    print("No content available for this page.")
else:
    link_parser = URLLinkParser()
    link_parser.feed(content)
    print("Links found on the page:")
    for link in link_parser.found_links:
        print(link)
