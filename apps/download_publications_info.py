import concurrent.futures
import os
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from config.dir_path import chrome_driver
from .params import DownloadPublicationsInfoParams as params
from .paper import Paper


class DownloadPublicationsInfo(object):

    _TIMEOUT = 15
    _MAX_WORKERS = 3

    def __init__(
        self,
        input_dir,
        target_dir,
        xlsx_service
    ):
        self._input_dir = input_dir
        self._target_dir = target_dir
        self._xlsx_service = xlsx_service

    def execute(self):
        departments = self._find_all_departments()
        with concurrent.futures.ThreadPoolExecutor(
           max_workers=self._MAX_WORKERS) as executor:
            for d in departments:
                files = os.listdir(self._input_dir + d)
                for filename in files:
                    output_path = self._target_dir + d + "/" + \
                        filename[:-4] + "link.xlsx"
                    executor.submit(
                        self._get_papers_information,
                        self._input_dir + d + "/" + filename,
                        output_path
                    )

    def _find_all_departments(self):
        departments = []
        dirs = os.listdir(self._input_dir)
        for ddir in dirs:
            fullpath = os.path.join(self._input_dir, ddir)
            if os.path.isdir(fullpath) and not ddir.startswith('.') and \
               not os.path.exists(self._target_dir + ddir):
                os.mkdir(self._target_dir + ddir)
                departments.append(ddir)
        return departments

    def _get_papers_information(self, input_path, output_path):

        urls = pd.read_excel(input_path)["題名網址"].to_list()
        papers = []

        for url in urls:
            driver = webdriver.Chrome(chrome_driver)
            paper = self._get_paper(url, driver)
            if paper:
                print(paper)
                papers.append(paper)
            driver.close()
        print(len(papers))
        self._xlsx_service.produce_paper_info_excel(papers, output_path)

    def _get_paper(self, url, driver):
        driver.get(url+"?locale=zh-TW")
        html = driver.page_source

        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", {"class": "itemDisplayTable"})
        if not table:
            return None
        paper: Paper = _to_paper(table)
        citation = soup.find("div", {"class": "citation"})
        if citation and citation["style"] != "display:none":
            try:
                element = WebDriverWait(driver, self._TIMEOUT).until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        params.citation_xpath
                    ))
                )
                paper.citation = element.text
                paper.citation_url = element.find_element_by_tag_name("a")\
                    .get_attribute("href")
            except Exception as e:
                print(e)
                print("timeout")
        return paper


def _to_paper(table) -> Paper:
    paper = Paper()
    trs = table.find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        if "題名" in tds[0].text:
            paper.title = tds[1].get_text()
        elif "作者" in tds[0].text:
            paper.authors = tds[1].get_text()
        elif "教師" in tds[0].text:
            paper.teacher = tds[1].get_text()
        elif "日期" in tds[0].text:
            paper.date = tds[1].get_text()
        elif "出版者" in tds[0].text:
            paper.publisher = tds[1].get_text()
        elif "關聯" in tds[0].text:
            paper.relation = tds[1].get_text()
        elif "關鍵詞" in tds[0].text:
            paper.key_words = tds[1].get_text()
        elif "摘要" in tds[0].text:
            paper.abstract = tds[1].get_text()
    return paper
