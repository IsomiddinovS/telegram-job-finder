import json
import sys
import requests
import xml.etree.ElementTree as ET
from pathlib import Path
from html.parser import HTMLParser

JOBS_FILE = "jobs.json"

class HTMLStripper(HTMLParser):
    """Remove HTML tags from text"""
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []
    
    def handle_data(self, data):
        self.text.append(data)
    
    def get_data(self):
        return ' '.join(self.text).strip()

def strip_html(html_text):
    """Strip HTML tags from text"""
    if not html_text or html_text == 'N/A':
        return html_text
    try:
        stripper = HTMLStripper()
        stripper.feed(html_text)
        return stripper.get_data()
    except:
        return html_text

def collect():
    """Fetch jobs from RSS feeds and save to jobs.json"""
    print("Collecting jobs from RSS feeds...")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        
        feeds = [
            "https://weworkremotely.com/categories/remote-programming-jobs.rss",
            "https://weworkremotely.com/categories/remote-devops-sysadmin-jobs.rss"
        ]
        
        jobs = []
        
        for feed_url in feeds:
            response = requests.get(feed_url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # Parse RSS/XML feed
            root = ET.fromstring(response.content)
            
            # Extract items from RSS feed
            for item in root.findall('.//item'):
                title = item.findtext('title', 'N/A')
                link = item.findtext('link', 'N/A')
                description = item.findtext('description', 'N/A')
                
                # Strip HTML tags from description
                description = strip_html(description)
                
                jobs.append({
                    'title': title,
                    'link': link,
                    'description': description
                })
        
        with open(JOBS_FILE, 'w') as f:
            json.dump(jobs, f, indent=2)
        
        print(f"✓ Saved {len(jobs)} jobs to {JOBS_FILE}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def search(keywords):
    """Search jobs by multiple keywords in title and description"""
    if not Path(JOBS_FILE).exists():
        print(f"Error: {JOBS_FILE} not found. Run 'python main.py collect' first.")
        sys.exit(1)
    
    with open(JOBS_FILE, 'r') as f:
        jobs = json.load(f)
    
    # Convert keywords to lowercase
    keywords_lower = [k.lower() for k in keywords]
    results = []
    
    for job in jobs:
        title = str(job.get('title', '')).lower()
        description = str(job.get('description', '')).lower()
        content = title + ' ' + description
        
        # Count how many keywords match
        matches = sum(1 for kw in keywords_lower if kw in content)
        
        # Only include jobs that match at least one keyword
        if matches > 0:
            results.append((matches, job))
    
    # Sort by matches (descending) for relevance ranking
    results.sort(key=lambda x: x[0], reverse=True)
    
    keywords_str = ' '.join(keywords)
    print(f"\nFound {len(results)} job(s) matching '{keywords_str}':\n")
    
    for i, (matches, job) in enumerate(results[:10], 1):
        title = job.get('title', 'N/A')
        link = job.get('link', 'N/A')
        description = job.get('description', 'N/A')
        
        # Limit description to 200 characters
        if len(description) > 200:
            description = description[:200].rstrip() + '...'
        
        score = f"[{matches}/{len(keywords_lower)}]"
        print(f"{i}. {score} {title}")
        print(f"   Link: {link}")
        if description != 'N/A':
            print(f"\n   Description:")
            print(f"   {description}")
        print()

def main():
    if len(sys.argv) < 2:
        print("Job Finder - Find remote jobs")
        print("\nUsage:")
        print("  python main.py collect                          - Fetch jobs from RSS feeds")
        print("  python main.py search <keyword1> [keyword2] ... - Search for jobs by keywords")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "collect":
        collect()
    elif command == "search":
        if len(sys.argv) < 3:
            print("Usage: python main.py search <keyword1> [keyword2] ...")
            sys.exit(1)
        search(sys.argv[2:])
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
