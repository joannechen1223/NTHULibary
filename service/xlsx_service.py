import time
import urllib.request
import pandas as pd
from bs4 import BeautifulSoup


class XlsService(object):

    _SLEEP_SEC = 5
    _prefix = "http://nthur.lib.nthu.edu.tw"
    _headers = {"Accept-Language": "zh-TW"}
    _sheet_name = "工作表1"

    def __init__(self):
        self._reset()

    def produce_excel(self, url, output_path):
        self._reset()
        req = urllib.request.Request(url, headers=self._headers)
        page = urllib.request.urlopen(req)

        time.sleep(self._SLEEP_SEC)
        table = BeautifulSoup(
            page, "html.parser"
        ).find('table', {'class': 'displaytag'})

        if table:
            trs = table.find_all("tr")[1:]
            for tr in trs:
                tds = tr.find_all("td")
                row = []
                for i in range(len(tds)):
                    row.append(
                        tds[i].text.replace("\n", "").replace("\xa0", "")
                    )
                    if i == 0:
                        row.append("")
                    elif i == 2:
                        row = self._add_paper_url(tds[i], row)
                    elif i == 4:
                        self._add_hyperlink(tds[i])
                self._rows.append(row)

        self._to_excel(
            output_path=output_path,
            columns=["類別", "", "日期", "題名", "", "題名網址", "作者", "檔案"],
            col_width=[13, 0, 0, 150, 0, 55, 150, 0],
            hyperlink_char="H"
        )

    def produce_principle_excel(self, url, output_path, pgs):
        self._reset()
        for pg in range(pgs):
            print(output_path, url+"?itemsPerPage=50&page="+str(pg))
            req = urllib.request.Request(
                url+"?itemsPerPage=50&page="+str(pg),
                headers=self._headers
            )
            page = urllib.request.urlopen(req)

            time.sleep(self._SLEEP_SEC)
            soup = BeautifulSoup(page, 'html.parser')
            table = soup.find('table', {'class': 'object_table'})

            if table:
                trs = table.find_all('tr')[1:]
                for tr in trs:
                    tds = tr.find_all('td')
                    row = []
                    for i in range(len(tds)):
                        row.append(
                            tds[i].text.replace("\n", "").replace("\xa0", "")
                        )
                        if i == 1:
                            row = self._add_paper_url(tds[i], row)
                        elif i == 3:
                            self._add_hyperlink(tds[i])
                    self._rows.append(row)

        self._to_excel(
            output_path=output_path,
            columns=["日期", "題名", "", "題名網址", "作者", "檔案"],
            col_width=[0, 150, 0, 55, 150, 0],
            hyperlink_char="F"
        )

    def produce_paper_info_excel(self, papers, output_path):
        self._reset()
        self._rows = [p.to_list() for p in papers]
        self._to_excel(
            output_path=output_path,
            columns=[
                "題名", "作者", "教師", "日期", "出版者", "關聯",
                "關鍵詞", "摘要", "引用次數", "引用次數連結"
            ],
            col_width=[100, 50, 0, 0, 30, 100, 50, 150, 0, 100],
        )

    def _reset(self):
        self._rows = []
        self._imgs = []
        self._links = []

    def _add_paper_url(self, elem, row):
        row.append("")
        row.append(
            self._prefix + elem.find_all("a")[0].get("href")
        )
        return row

    def _add_hyperlink(self, elem):
        img = ""
        link = ""
        if len(elem.find_all("img")) > 0:
            img = elem.find_all("img")[0].get("src")
            link = elem.find_all("a")[0].get("href")
        print(img, link)
        if "hyperlink" in img:
            self._imgs.append("hyperlink")
        elif "pdf" in img:
            self._imgs.append("pdf")
        else:
            self._imgs.append("")
        self._links.append(self._prefix + link)

    def _to_excel(self, output_path, columns, col_width, hyperlink_char=""):
        df = pd.DataFrame(data=self._rows, columns=columns)
        print(df.head)

        writer = pd.ExcelWriter(output_path, engine="xlsxwriter")
        df.to_excel(writer, sheet_name=self._sheet_name, index=False)
        worksheet = writer.sheets[self._sheet_name]

        # set column width
        for idx, col in enumerate(df):
            if col_width[idx]:
                worksheet.set_column(idx, idx, col_width[idx])

        # add hyperlink
        if self._imgs:
            for idx, row in df.iterrows():
                if self._imgs[idx]:
                    worksheet.write_url(
                        hyperlink_char + str(idx+2),
                        self._links[idx],
                        string=self._imgs[idx]
                    )
        writer.save()
        writer.close()
