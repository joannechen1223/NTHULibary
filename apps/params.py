class DownloadPublicationsListParams(object):
    entrance_url = "http://nthur.lib.nthu.edu.tw:8080/teacher/searchbycollection.php"
    block_xpath_prefix = "/html/body/table/tbody/tr[3]/td[2]/table/tbody/tr/"
    college_block_xpath_list = [
        "td[1]/table/tbody/tr[1]",  # 理學院
        "td[1]/table/tbody/tr[3]",  # 工學院
        "td[1]/table/tbody/tr[5]",  # 電機資訊學院
        "td[1]/table/tbody/tr[7]",  # 人文社會學院
        "td[2]/table/tbody/tr[1]",  # 生命科學院
        "td[2]/table/tbody/tr[3]",  # 原子科學院
        "td[2]/table/tbody/tr[5]",  # 科技管理學院
        "td[2]/table/tbody/tr[7]"   # 共同教育委員會
    ]
    principle_block_xpath = "td[1]/table/tbody/tr[9]"   # 歷任校長
    department_xpath_format = "/td[2]/a[%d]"
    professor_table_xpath = "/html/body/table/tbody/tr[3]/td[2]/table"
    professor_xpath_format = professor_table_xpath + "/tbody/tr[%d]/td[2]/a"
    professor_paper_list_xpath = "/html/body/table/tbody/tr[3]/td[1]/table[2]/tbody/tr[2]/td/table[2]/tbody/tr[1]/td/a"


class DownloadPublicationsInfoParams(object):
    citation_xpath = "//*[@id=\"ISI\"]/table/tbody/tr[1]/td[2]"
