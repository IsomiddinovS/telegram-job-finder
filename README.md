# Job Finder

A minimal remote job finder using the RemoteOK API.

## Requirements

- Python 3.6+
- requests library only

## Setup

```bash
pip install -r requirements.txt
```

## Usage

### Collect Jobs

Fetch all available jobs from RemoteOK and save to `jobs.json`:

```bash
python main.py collect
```

This creates a `jobs.json` file with all current remote jobs.

### Search Jobs

Search for jobs by keyword in title, description, and tags:

```bash
python main.py search python
python main.py search javascript
python main.py search senior
```

Search results show the first 10 matches with job title, company, and tags.

## How It Works

1. **Collect**: Fetches jobs from `https://remoteok.io/api`, filters valid job entries, and saves to `jobs.json`
2. **Search**: Reads `jobs.json` and searches for your keyword across title, description, and tags fields
3. **No dependencies**: Only uses Python standard library and `requests` for HTTP calls

## Project Size

- **main.py**: ~75 lines
- **requirements.txt**: 1 line
- **Total Python code**: Under 150 lines
