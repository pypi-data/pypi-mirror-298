import time
import random
import argparse
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from .web_crawler import WebCrawler
from .text_processor import TextProcessor
from .document_generator import DocumentGenerator

class NovelCrawlerService:
    """
    A service class for crawling and processing web novels.

    Attributes:
        novel_url (str): The URL of the novel to crawl.
        start_chapter (int): The starting chapter number.
        end_chapter (int): The ending chapter number.
        output_dir (str): The directory where the output files will be saved.
        num_workers (int): The number of worker threads to use for crawling.
        allow_non_english (bool): Flag to allow non-English content. Default is False.
        crawler (WebCrawler): An instance of the WebCrawler class for fetching web pages.
        processor (TextProcessor): An instance of the TextProcessor class for processing text.
        title (str): The title of the novel.
        author (str): The author of the novel.
        base_url (str): The base URL for the novel chapters.
        doc_generator (DocumentGenerator): An instance of the DocumentGenerator class for generating documents.

    Methods:
        __init__(novel_url, start_chapter, end_chapter, output_dir, num_workers, allow_non_english=False):
            Initializes the NovelCrawlerService with the given parameters.
        
        extract_novel_info():
            Extracts the novel title, author, and base URL from the novel URL.
        
        process_chapter(current_chapter):
            Processes a single chapter by fetching its content and cleaning the text.
        
        crawl_novel():
            Crawls the novel from the start chapter to the end chapter and generates a PDF document.
    """
    def __init__(self, novel_url, start_chapter, end_chapter, output_dir, num_workers, allow_non_english=False):
        self.novel_url = novel_url
        self.start_chapter = start_chapter
        self.end_chapter = end_chapter
        self.output_dir = output_dir
        self.num_workers = num_workers
        self.allow_non_english = allow_non_english
        self.crawler = WebCrawler(self.allow_non_english)
        self.processor = TextProcessor()
        self.title, self.author, self.base_url = self.extract_novel_info()
        if not self.title or not self.author or not self.base_url:
            raise ValueError("Failed to extract novel title, author, or base URL.")
        self.doc_generator = DocumentGenerator(self.title, self.author)

    def extract_novel_info(self):
        html = self.crawler.fetch_page(self.novel_url)
        if html:
            title, author = self.crawler.extract_novel_info(html)
            base_url = self.novel_url.replace('https://freewebnovel.com', 'https://read.freewebnovel.me')
            base_url = base_url.replace('.html','')
            print(base_url)
            return title, author, base_url
        return None, None, None

    def process_chapter(self, current_chapter):
        current_url = f"{self.base_url}/chapter-{current_chapter}"
        print(f"Crawling {current_url}...")
        html = self.crawler.fetch_page(current_url)
        if html:
            text = self.crawler.extract_text_from_article(html)
            if text:
                text = self.processor.remove_non_utf8_characters(text)
                chapter_heading = f"Chapter {current_chapter}"
                text = text.replace(chapter_heading, '', 1).strip()
                return (current_chapter, chapter_heading, text)
            else:
                print(f"Chapter {current_chapter} not found.")
        else:
            print(f"Failed to fetch {current_url}")
        return None

    def crawl_novel(self):
        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            futures = []
            for current_chapter in range(self.start_chapter, self.end_chapter + 1):
                futures.append(executor.submit(self.process_chapter, current_chapter))
                time.sleep(random.uniform(0.5, 1.5))

            results = []
            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)

        results.sort(key=lambda x: x[0])

        for _, chapter_heading, text in results:
            self.doc_generator.add_chapter(chapter_heading, text)

        output_file = os.path.join(self.output_dir, self.title)
        self.doc_generator.generate_pdf(output_file, clean_tex=True)

def main():
    parser = argparse.ArgumentParser(description="Crawl a web novel and generate a PDF.")
    parser.add_argument('novel_url', type=str, help='The FreeWebNovel URL of the novel to crawl.')
    parser.add_argument('start_chapter', type=int, help='The starting chapter number.')
    parser.add_argument('end_chapter', type=int, help='The ending chapter number.')
    parser.add_argument('--output_dir', type=str, default=os.getcwd(), help='The destination directory for the generated PDF.')
    parser.add_argument('--num-workers', type=int, default=10, help='The number of workers to use for crawling.')
    parser.add_argument('--allow-non-english', action='store_true', help='Allow non-English characters in the novel title and author name.')
    args = parser.parse_args()
    print("Output directory: ", args.output_dir)
    service = NovelCrawlerService(args.novel_url, args.start_chapter, args.end_chapter, args.output_dir, args.num_workers, args.allow_non_english)
    service.crawl_novel()

if __name__ == "__main__":
    main()