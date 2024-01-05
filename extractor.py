import os
import requests
from bs4 import BeautifulSoup

class DataExtractor:
    def __init__(self, output_directory):
        self.output_directory = output_directory

    def extract_article(self, url, output_filename):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract article title without unwanted text
            title = soup.title.text.strip().replace('- Blackcoffer Insights', '')

            # Extract article text
            article_paragraphs = soup.find_all('p')
            article_text = ' '.join([p.text.strip() for p in article_paragraphs])

            # Remove the unwanted footer information
            footer_text = "Contact us: hello@blackcoffer.com © All Right Reserved, Blackcoffer(OPC) Pvt. Ltd"
            article_text = article_text.replace(footer_text, '')

            # Print the full output file path
            full_output_path = os.path.join(self.output_directory, output_filename)
            print(f"Output Filename: {full_output_path}")

            # Write to the file
            with open(full_output_path, 'w', encoding='utf-8') as file:
                file.write(f"{title}\n\n{article_text}")
            
            return title, article_text
        except Exception as e:
            print(f"Error extracting {url}: {e}")
            return None, None


