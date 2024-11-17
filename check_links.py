import re
import requests
from pathlib import Path
import concurrent.futures
import sys

def extract_links_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Match markdown links [text](url) and bare URLs
    urls = re.findall(r'\[([^\]]+)\]\(([^)]+)\)|(?<![\(\[])(https?://[^\s\)]+)', content)
    # Flatten and clean the results
    links = []
    for match in urls:
        if isinstance(match, tuple):
            # If it's a markdown link, take the URL part
            link = match[1]
        else:
            # If it's a bare URL
            link = match
        # Remove any trailing punctuation that might have been caught
        link = re.sub(r'[.,;:]$', '', link)
        links.append(link)
    return links

def check_link(url):
    try:
        # Only check http(s) links
        if not url.startswith(('http://', 'https://')):
            return url, 'skipped'

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.head(url, allow_redirects=True, timeout=10, headers=headers)
        if response.status_code == 405:  # Method not allowed
            response = requests.get(url, allow_redirects=True, timeout=10, headers=headers)
        return url, response.status_code
    except Exception as e:
        return url, str(e)

def main():
    docs_dir = Path('docs')
    md_files = list(docs_dir.rglob('*.md'))
    all_links = []

    print("Checking links in markdown files...")
    for file_path in md_files:
        links = extract_links_from_file(file_path)
        if links:
            print(f"\nLinks found in {file_path}:")
            all_links.extend(links)
            for link in links:
                print(f"  {link}")

    print("\nVerifying links...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(check_link, set(all_links)))

    broken_links = []
    for url, status in results:
        if isinstance(status, int):
            if status >= 400:
                print(f"❌ {url} - Status: {status}")
                broken_links.append((url, status))
            else:
                print(f"✅ {url} - Status: {status}")
        else:
            print(f"❌ {url} - Error: {status}")
            broken_links.append((url, status))

    if broken_links:
        print("\nBroken links found:")
        for url, status in broken_links:
            print(f"- {url} (Status/Error: {status})")
        sys.exit(1)
    else:
        print("\nAll links are valid!")
        sys.exit(0)

if __name__ == '__main__':
    main()
