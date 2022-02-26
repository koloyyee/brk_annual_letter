import os
import re
import shutil
import urllib.request
from typing import List

import pdfkit
import urllib3
from bs4 import BeautifulSoup as bs


class Letters():
    BRK_letters = "https://www.berkshirehathaway.com/letters/"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}

    def fetch(self):
        http = urllib3.PoolManager()

        r = http.request(method = "GET", url = f"{self.BRK_letters}letters.html", headers= self.headers)

        body = bs(r.data, "html.parser")


        a_tags = body.find_all("a", href= True)
        letter_urls = []
        for a in a_tags:
            letter_urls.append(a["href"])

        # converting to url
        # e.g: https://www.berkshirehathaway.com/letters/1990.html
        letters = letter_urls[1:-1]
        target = [f"{self.BRK_letters}{letter}" for letter in letters]
        
        self.html_to_pdf(target)


    # separate the html and pdfs
    def html_to_pdf(self, target_urls: List) -> None:
        years = self.years_names(target_urls)
        if not os.path.exists("./warren's letters"):
            os.makedirs("./warren's letters")
        for i, t in enumerate(target_urls):
            file = f"./warren's letters/{years[i]}.pdf"
            if "html" in t:
                if not os.path.exists(file):
                    pdfkit.from_url(t, file)
                    print(f"downloaded {file}.")
                else:
                    print(f"{file} existed")
            elif "pdf" in t:
                if not os.path.exists(file):
                    with urllib.request.urlopen(t) as response, open(file, "wb") as pdf_file:
                        shutil.copyfileobj(response, pdf_file)
                        print(f"downloaded {file}.")
                else:
                    print(f"{file} existed")


    def years_names(self, target_urls: List) -> List :
        years = []
        for t in target_urls:
            result = re.findall(pattern =r"[0-9]", string=t)
            year = "".join(result)
            years.append(year)
        return years
