import json
import sys
import requests
import xml.etree.ElementTree as ET
from pathlib import Path

JOBS_FILE = "jobs.json"

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

def search(keyword):
    """Search jobs by keyword in title and description"""
    if not Path(JOBS_FILE).exists():
        print(f"Error: {JOBS_FILE} not found. Run 'python main.py collect' first.")
        sys.exit(1)
    
    with open(JOBS_FILE, 'r') as f:
        jobs = json.load(f)
    
    keyword = keyword.lower()
    results = []
    
    for job in jobs:
        title = str(job.get('title', '')).lower()
        description = str(job.get('description', '')).lower()
        
        if keyword in title or keyword in description:
            results.append(job)
    
    print(f"\nFound {len(results)} job(s) matching '{keyword}':\n")
    
    for i, job in enumerate(results[:10], 1):
        print(f"{i}. {job.get('title', 'N/A')}")
        print(f"   Link: {job.get('link', 'N/A')}")
        print(f"   Description: {job.get('description', 'N/A')[:100]}...")
        print()

def main():
    if len(sys.argv) < 2:
        print("Job Finder - Find remote jobs")
        print("\nUsage:")
        print("  python main.py collect          - Fetch jobs from RemoteOK API")
        print("  python main.py search <keyword> - Search for jobs by keyword")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "collect":
        collect()
    elif command == "search":
        if len(sys.argv) < 3:
            print("Usage: python main.py search <keyword>")
            sys.exit(1)
        search(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
