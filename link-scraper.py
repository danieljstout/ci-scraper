#!/usr/bin/env python
# Use python3 for this script

import re
import json
import urllib.request
import bs4

domain = "witkindesign.com"
base_url = "https://" + domain
internal_links = [base_url]
ciwork_links = {}
insecure_links = {}
external_links = []
hash_links = []
relative_links = []
visited_links = []
asset_links = []

def url_to_soup(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()
    soup = bs4.BeautifulSoup(html, features="lxml")
    return soup

def organize_links(link, current_url):
    href = link['href']
    if f"pt.{domain}" in href or f"es.{domain}" in href:
        pass
    elif "wp-content/uploads" in href:
        if "ciwork.co" in href:
            a_dict = {href, f"{link}"}
            if current_url in ciwork_links:
                ciwork_links[current_url].append(a_dict)
            else:
                ciwork_links[current_url] = [a_dict]
        asset_links.append(href)
    elif "#" in href:
        hash_links.append(link)
    elif "ciwork.co" in href:
        a_dict = {href, f"{link}"}
        if current_url in ciwork_links:
            ciwork_links[current_url].append(a_dict)
        else:
            ciwork_links[current_url] = [a_dict]
    elif domain in href:
        internal_links.append(href)
    elif re.compile(r'(https?://[^\s]+)').search(href):
        external_links.append(href)
    else:
        relative_links.append(href)
        internal_links.append(f"{base_url}{href}")

def get_all_links_on_page(url):
    try:
        for a in url_to_soup(url).find_all('a', href=True):
            organize_links(a, url)
    except:
        print(f"An error occurred when attempting to visit {url}")
    finally:
        return

def visit_all_pages():
    for link in set(internal_links):
        if link not in visited_links:
            get_all_links_on_page(link)
            visited_links.append(link)
            visit_all_pages()

def main():
    visit_all_pages()
    print(f"asset_links count: {len(asset_links)}")
    print("\n")
    print(f"internal_links count {len(internal_links)}")
    print("\n")
    print(f"external_links count: {len(external_links)}")
    print("\n")
    print(f"hash_links count: {len(hash_links)}")
    print("\n")
    print(f"relative_links count: {len(relative_links)}")
    print("\n")
    print(f"total unique links visited: {len(visited_links)}")

    ciwork_links_count = 0
    print("remaining ciwork links")
    for arr in ciwork_links:
        print(arr)
        print(ciwork_links[arr])
        ciwork_links_count += len(ciwork_links[arr])
    print(f"ciwork_links count: {ciwork_links_count}")

if __name__ == "__main__":
    main()