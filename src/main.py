import arxivscraper
import pprint
import os
import re
import qrcode
from PIL import Image, ImageDraw, ImageFont
from typing import List, Tuple
import textwrap
import time



WIFI_ON_ICON = "icons/wifi-icon.png"
WIFI_OFF_ICON = "icons/wifi-off-icon.png"







class ArxivScraper:
    def __init__(self, category: str, date_from: str, date_until: str):
        self.category = category
        self.date_from = date_from
        self.date_until = date_until
        # self.scraper = arxivscraper.Scraper(category=self.category, date_from=self.date_from, date_until=self.date_until)
        self.scraper = arxivscraper.Scraper(category=self.category)
        self.output = self.scraper.scrape()
        self.parsed_output = []

    def create_folder_name(self, paper: dict) -> str:
        paper_name = paper['title']
        paper_name = ' '.join(paper_name.split())
        folder_name = ' '.join([word.capitalize() for word in paper_name.split(' ')])
        folder_name = re.sub(r'[^\w\s-]', '', folder_name).strip().encode('ascii', 'ignore').decode('ascii')
        folder_name = f"{paper['updated'] or paper['created']}_{folder_name}"
        folder_name = os.path.join(self.category, folder_name)
        return folder_name

    def create_qr(self, url: str, folder_path: str) -> None:
        pdf_path = url.replace("abs", "pdf")+".pdf"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(pdf_path)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").resize((72,72))
        img.save(os.path.join(folder_path, 'qr.png'))

    def create_new_image(self, paper: dict, qr_image: Image) -> Image:
        new_image = Image.new('RGB', (400, 300), color='white')
        draw = ImageDraw.Draw(new_image)
        font = ImageFont.truetype("arial.ttf", 12)
        current_time = time.strftime("%H:%M")
        draw.text((350, 4), f'{current_time}', font=font, fill='black')
        draw.line((10, 18, 400-10, 18), fill='black', width=1)
        draw.line((10, 75-2, 400-10, 75-2), fill='black', width=1)


        # draw.ellipse((15, 5, 25, 15), fill='black')
        wifi_icon = Image.open(WIFI_ON_ICON).resize((15, 15))
        new_image.paste(wifi_icon, (15, 5))


        # dynamic scale text size and new line in order to fit into 400 screen width
        font_size = 16
        text = self.create_folder_name(paper).split("_", 1)[1]
        # while ImageFont.truetype("arialbd.ttf", font_size).getsize(text)[0] > 800:
            # font_size -= 4

        # wrap the text to fit within 400 width
        wrapped_text = textwrap.wrap(text, width=50)
        font_size -= len(wrapped_text)
        # draw the text on the image
        y = 30
        for line in wrapped_text:
            draw.text((10, y), line, font=ImageFont.truetype("arialbd.ttf", font_size), fill='black')
            y += font_size



        font_size = 12
        abstract = paper['abstract']
        abstract = abstract[0].upper() + abstract[1:]
        abstract_words = abstract.split()
        abstract_lines = [' '.join(abstract_words[i:i+20]) for i in range(0, len(abstract_words), 20)]
        abstract = '\n'.join(abstract_lines)
        wrapped_text = textwrap.wrap(abstract, width=68)
        y = 75

        for line in wrapped_text:
            if wrapped_text.index(line) == 11:
                text = line + "..."
                draw.text((10, y), text, font=font, fill='black')
                break
            draw.text((10, y), line, font=font, fill='black')
            y += font_size +0.5

        
        # draw.text((10, 225), f'Authors:', font=font, fill='black', weight='bold')


        # Draw footers, Authors, Date, and Categories
        font_size = 12
        text = ", ".join(paper["authors"][:-1])
        text = " ".join([word.capitalize() for word in text.split()])
        text = "Authors: " + text
        wrapped_text = textwrap.wrap(text, width=45)

        y = 235
        for line in wrapped_text:
            if wrapped_text.index(line) >= 1:
                text = line + "..."
                draw.text((55, y), line, font=ImageFont.truetype("arial.ttf", font_size), fill='black')
                break
            else:
                draw.text((10, y), line, font=ImageFont.truetype("arial.ttf", font_size), fill='black')
            y += font_size

        draw.text((10, 265), f'Created: {paper["created"]}, Updated:{paper["updated"]}', font=font, fill='black')
        draw.text((10, 280), f'Categories: {paper["categories"]}', font=font, fill='black')
        new_image.paste(qr_image, (325, 225))
        return new_image

    def write_meta_file(self, paper: dict, folder_path: str) -> None:
        with open(os.path.join(folder_path, 'meta.txt'), 'w', encoding='utf-8') as f:
            f.write(f'Title: {paper["title"]}\n\n')
            abstract = paper['abstract']
            abstract_words = abstract.split()
            abstract_lines = [' '.join(abstract_words[i:i+20]) for i in range(0, len(abstract_words), 20)]
            abstract = '\n'.join(abstract_lines)
            f.write(f'Abstract: {abstract}\n\n')
            f.write(f'Authors: {", ".join(paper["authors"])}\n\n')
            f.write(f'ID: {self.create_folder_name(paper).split("_", 1)[1]}\n')
            f.write(f'Created: {self.create_folder_name(paper).split("_", 1)[0]}\n')
            f.write(f'Categories: {paper["categories"]}\n')
            f.write(f'URL: https://arxiv.org/abs/{self.create_folder_name(paper).split("_", 1)[1]}\n\n')
            f.write(f'PDF_URL: https://arxiv.org/pdf/{self.create_folder_name(paper).split("_", 1)[1]}.pdf\n\n')

    def generate_qr_codes(self) -> None:
        for paper in self.output:
            folder_name = self.create_folder_name(paper)
            folder_path = os.path.join('d:/arxivs/CS/', folder_name, )
            os.makedirs(folder_path, exist_ok=True)
            self.parsed_output.append((paper['title'], paper['abstract'], paper['authors']))
            if not os.path.exists(os.path.join(folder_path, 'qr.png')):
                self.create_qr(paper["url"], folder_path)
            qr_image = Image.open(os.path.join(folder_path, 'qr.png'))
            new_image = self.create_new_image(paper, qr_image)
            new_image.save(os.path.join(folder_path, 'screen.png'))
            self.write_meta_file(paper, folder_path)
        
def main():
    import argparse
    parser = argparse.ArgumentParser(description='Scrape arXiv papers and generate QR codes for their PDF URLs')
    parser.add_argument('--category', type=str, default='cs', help='arXiv category to scrape papers from')
    parser.add_argument('--date', type=str, default='2023-04-12', help='date to scrape papers from (format: YYYY-MM-DD)')
    parser.add_argument('--qr', action='store_true', help='generate QR codes for the PDF URLs')
    args = parser.parse_args()
    CATEGORY = args.category
    # DATE_FROM = "2023-05-05"
    DATE_FROM = args.date
    # DATE_UNTIL = "2023-05-05"
    DATE_UNTIL = args.date
    scraper = ArxivScraper(category=CATEGORY, date_from=DATE_FROM, date_until=DATE_UNTIL)
    scraper.generate_qr_codes()

if __name__ == '__main__':
    main()

