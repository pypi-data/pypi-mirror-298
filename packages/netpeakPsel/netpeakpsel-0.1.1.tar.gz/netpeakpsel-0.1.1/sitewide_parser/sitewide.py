import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import csv
from tqdm import tqdm
import lxml.etree as ET
import time
import os

class RequestHandler:
    def __init__(self, delay=1):
        self.delay = delay

    def make_request(self, url):
        """Выполняет HTTP-запрос с задержкой."""
        try:
            time.sleep(self.delay)  # Задержка перед запросом
            response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе {url}: {e}")
            return None

class CacheManager:
    def __init__(self, cache_file='cache.txt'):
        self.cache_file = cache_file
        self.cache = self.load_cache()

    def load_cache(self):
        """Загружает кеш из текстового файла."""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                return set(line.strip() for line in f)
        return set()

    def save_cache(self):
        """Сохраняет обновленный кеш в текстовый файл."""
        with open(self.cache_file, 'w') as f:
            for url in self.cache:
                f.write(f"{url}\n")

    def check_cache(self, url):
        """Проверяет, был ли URL уже обработан."""
        return url in self.cache

    def update_cache(self, url):
        """Добавляет новый URL в кеш."""
        self.cache.add(url)
        self.save_cache()

class Crawler:
    def __init__(self, request_handler, cache_manager):
        self.request_handler = request_handler
        self.cache_manager = cache_manager
        self.sitewide_elements = ['header', 'footer', 'nav', 'aside']

    def ensure_scheme(self, url):
        """Добавляет https:// к URL, если схема отсутствует."""
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            # Если схема отсутствует, добавляем https://
            print(f"Invalid URL '{url}': No scheme supplied. Adding https://")
            return f"https://{url}"
        return url


    def normalize_domain(self, url):
        """Нормализует домен, убирая 'www.'."""
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain

    def is_external_link(self, link, base_url):
        """Проверяет, является ли ссылка внешней."""
        domain_link = self.normalize_domain(link)
        domain_base = self.normalize_domain(base_url)
        return domain_link != domain_base

    def get_xpath(self, element):
        """Возвращает XPath элемента."""
        return element.getroottree().getpath(element)

    def get_sitewide_external_links(self, url):
        """Извлекает внешние ссылки из sitewide-элементов."""
        if self.cache_manager.check_cache(url):
            print(f"Страница {url} уже в кеше, пропускаем.")
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
        """Парсит один URL и сохраняет результат в шаблонизированный CSV файл для каждого домена."""
        # Нормализуем URL и домен
        url = self.ensure_scheme(url)
        domain = self.normalize_domain(url)
        
        # Создаем имя выходного файла для домена
        output_file = f"{domain}_sitewide_links.csv"
        
        print(f"Парсим {url} и сохраняем результат в {output_file}...")

        # Открываем CSV-файл с шаблонизированным именем для этого домена
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['Domain', 'External Link', 'XPath', 'Page URL'])
            
            # Извлекаем и записываем внешние ссылки
            external_links = self.get_sitewide_external_links(url)
            for link, xpath, page_url in external_links:
                csv_writer.writerow([url, link, xpath, page_url])

        print(f"Результаты для {url} сохранены в {output_file}")




    def parse_list_domain(self, domain_file, output='sitewide_external_links.csv'):
        """Парсит домены из файла и сохраняет результат в один общий CSV файл."""
        
        with open(domain_file, 'r') as f:
            domains = [line.strip() for line in f]

        # Открытие общего файла для записи
        with open(output, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Domain', 'External Link', 'XPath', 'Page URL'])

            # Цикл по доменам с использованием tqdm для отслеживания прогресса
            for domain in tqdm(domains, desc="Domain Scanning"):
                print(f"Парсим {domain}...")

                # Здесь вызываем ensure_scheme для каждого домена
                domain = self.ensure_scheme(domain)
                
                # Извлекаем и записываем данные для каждого домена в общий CSV файл
                external_links = self.get_sitewide_external_links(domain)
                for link, xpath, page_url in external_links:
                    writer.writerow([domain, link, xpath, page_url])

        print(f"Все результаты сохранены в {output}")

