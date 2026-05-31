import json
import sys
import requests
from pathlib import Path

JOBS_FILE = "jobs.json"

def collect():
    """Fetch jobs from RemoteOK API and save to jobs.json"""
    print("Collecting jobs from RemoteOK API...")
    try:
        response = requests.get("https://remoteok.io/api")
        response.raise_for_status()
        jobs = response.json()
        
        # Filter out non-job items (API returns metadata at index 0)
        jobs = [j for j in jobs if isinstance(j, dict) and 'title' in j]
        
        with open(JOBS_FILE, 'w') as f:
            json.dump(jobs, f, indent=2)
        
        print(f"✓ Saved {len(jobs)} jobs to {JOBS_FILE}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def search(keyword):
    """Search jobs by keyword in title, description, and tags"""
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
        tags = str(job.get('tag', '')).lower()
        
        if keyword in title or keyword in description or keyword in tags:
            results.append(job)
    
    print(f"\nFound {len(results)} job(s) matching '{keyword}':\n")
    
    for i, job in enumerate(results[:10], 1):
        print(f"{i}. {job.get('title', 'N/A')}")
        print(f"   Company: {job.get('company', 'N/A')}")
        print(f"   Tags: {job.get('tag', 'N/A')}")
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
