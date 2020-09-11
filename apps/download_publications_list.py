import os
import time
from .params import DownloadPublicationsListParams as params


class DownloadPublicationsList(object):

    _SLEEP_SEC = 1

    def __init__(
        self,
        target_dir,
        driver,
        xlsx_service
    ):
        self._target_dir = target_dir
        self._driver = driver
        self._xlsx_service = xlsx_service

    def execute(self):
        self._driver.get(params.entrance_url)
        for college_xpath in params.college_block_xpath_list:
            self._get_college_info(college_xpath)

    def _get_college_info(self, college_xpath):
        college_block = self._driver.find_element_by_xpath(
            params.block_xpath_prefix + college_xpath
        )
        college_name = college_block.find_element_by_tag_name("img") \
            .get_attribute("alt")
        department_len = len(college_block.find_elements_by_tag_name("a"))

        for d in range(department_len):
            self._get_department_info(
                idx=d,
                college_name=college_name,
                college_xpath=params.block_xpath_prefix + college_xpath
            )
            self._driver.back()
            time.sleep(self._SLEEP_SEC)

    def _get_department_info(self, idx, college_name, college_xpath):
        department = self._driver.find_element_by_xpath(
            college_xpath + params.department_xpath_format % (idx+1)
        )
        folder = self._target_dir + college_name + "-" + department.text
        if not os.path.exists(folder):
            os.mkdir(folder)

        department.click()
        time.sleep(self._SLEEP_SEC)
        professor_len = len(self._driver.find_elements_by_xpath(
            params.professor_table_xpath + "//a")
        )
        for p in range(professor_len):
            self._get_professor_info(
                idx=p,
                folder_name=folder
            )
            # self._driver.back()
            time.sleep(self._SLEEP_SEC)

    def _get_professor_info(self, idx, folder_name):
        professor = self._driver.find_element_by_xpath(
            params.professor_xpath_format % (idx+3)
        )
        professor_name = professor.text
        # professor.click()
        self._driver.get(professor.get_attribute("href"))
        time.sleep(self._SLEEP_SEC)
        print(professor_name)
        weburl = self._driver.find_element_by_xpath(
            params.professor_paper_list_xpath).get_attribute("href")
        self._driver.back()
        target_path = folder_name + "/" + professor_name + ".xlsx"
        if not os.path.exists(target_path):
            self._xlsx_service.produce_excel(weburl, target_path)
