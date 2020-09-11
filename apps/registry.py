from selenium import webdriver
from config.dir_path import (
    NTHU1,
    NTHU2,
    NTHU3,
    chrome_driver,
)
from service.xlsx_service import XlsService
from service.pdf_service import PdfService
from .download_pdf import DownloadPdfs
from .download_publications_info import DownloadPublicationsInfo
from .download_publications_list import DownloadPublicationsList


class Registry(object):

    _download_publications_list = None

    def download_publications_list(self):
        if not self._download_publications_list:
            self._download_publications_list = DownloadPublicationsList(
                target_dir=NTHU1,
                driver=webdriver.Chrome(chrome_driver),
                xlsx_service=XlsService()
            )
        return self._download_publications_list

    _download_publications_info = None

    def download_publications_info(self):
        if not self._download_publications_info:
            self._download_publications_info = DownloadPublicationsInfo(
                input_dir=NTHU1,
                target_dir=NTHU2,
                xlsx_service=XlsService()
            )
        return self._download_publications_info

    _download_pdfs = None

    def download_pdfs(self):
        if not self._download_pdfs:
            self._download_pdfs = DownloadPdfs(
                input_dir=NTHU1,
                target_dir=NTHU3,
                pdf_service=PdfService()
            )
        return self._download_pdfs


registry = Registry()
