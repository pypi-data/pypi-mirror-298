import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import csv
from tqdm import tqdm
import lxml.etree as ET
import time
import os
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class RequestHandler:
    def __init__(self, delay=1):
        self.delay = delay

    def make_request(self, url):
        """Performs HTTP request with delay."""
        try:
            time.sleep(self.delay)  # Delay before request
            response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}Error while requesting {url}: {e}")
            return None

class CacheManager:
    def __init__(self, cache_file='cache.txt'):
        self.cache_file = cache_file
        self.cache = self.load_cache()

    def load_cache(self):
        """Loads cache from a text file."""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                return set(line.strip() for line in f)
        return set()

    def save_cache(self):
        """Saves updated cache to a text file."""
        with open(self.cache_file, 'w') as f:
            for url in self.cache:
                f.write(f"{url}\n")

    def check_cache(self, url):
        """Checks if a URL has already been processed."""
        return url in self.cache

    def update_cache(self, url):
        """Adds a new URL to the cache."""
        self.cache.add(url)
        self.save_cache()

class Crawler:
    def __init__(self, request_handler, cache_manager):
        self.request_handler = request_handler
        self.cache_manager = cache_manager
        self.sitewide_elements = ['header', 'footer', 'nav', 'aside']

    def ensure_scheme(self, url):
        """Adds https:// to the URL if the scheme is missing."""
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            return f"https://{url}"
        return url

    def normalize_domain(self, url):
        """Normalizes the domain by removing 'www.' if present."""
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain

    def is_external_link(self, link, base_url):
        """Checks if the link is external compared to the base URL."""
        domain_link = self.normalize_domain(link)
        domain_base = self.normalize_domain(base_url)
        return domain_link != domain_base

    def get_xpath(self, element):
        """Returns the XPath of an element."""
        return element.getroottree().getpath(element)

    def get_sitewide_external_links(self, url):
        """Extracts external links from sitewide elements (header, footer, nav, aside)."""
        if self.cache_manager.check_cache(url):
            print(f"{Fore.WHITE}Page {Fore.YELLOW}{url} {Fore.WHITE}is already cached, skipping.")
            return set()

        response = self.request_handler.make_request(url)
        if response is None:
            return set()

        soup = BeautifulSoup(response.text, 'lxml')
        dom = ET.HTML(str(soup))

        external_links = set()
        for element in self.sitewide_elements:
            for tag in soup.find_all(element):
                for link in tag.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(url, href)
                    if self.is_external_link(full_url, url):
                        lxml_elements = dom.xpath(f"//a[@href='{href}']")
                        if lxml_elements:
                            link_xpath = self.get_xpath(lxml_elements[0])
                            external_links.add((full_url, link_xpath, url))

        self.cache_manager.update_cache(url)
        self.cache_manager.save_cache()
        return external_links

    def parse_url(self, url):
        """Parses a single URL and saves the result to a templated CSV file for each domain."""
        url = self.ensure_scheme(url)
        domain = self.normalize_domain(url)

        output_file = f"{domain}_sitewide_links.csv"
        print(f"{Fore.WHITE}Parsing {Fore.YELLOW}{url} {Fore.WHITE}and saving results to {output_file}...")

        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['Domain', 'External Link', 'XPath', 'Page URL'])

            external_links = self.get_sitewide_external_links(url)
            for link, xpath, page_url in external_links:
                csv_writer.writerow([url, link, xpath, page_url])

        print(f"{Fore.GREEN}Results for {Fore.YELLOW}{url} {Fore.GREEN}saved to {output_file}")

    def parse_list_domain(self, domain_file, output):
        """Parses domains from a file and saves the result to a single CSV file."""
        with open(domain_file, 'r') as f:
            domains = [line.strip() for line in f]

        with open(output, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Domain', 'External Link', 'XPath', 'Page URL'])

            for domain in tqdm(domains, desc="Scanning domains", bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.YELLOW, Fore.RESET)):
                domain = self.ensure_scheme(domain)
                external_links = self.get_sitewide_external_links(domain)
                for link, xpath, page_url in external_links:
                    writer.writerow([domain, link, xpath, page_url])


        print(f"{Fore.GREEN}All results saved to {output}")
