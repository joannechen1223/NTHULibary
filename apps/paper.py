from typing import List


class Paper(object):

    def __init__(self):
        self.title = ""
        self.authors = ""
        self.teacher = ""
        self.date = ""
        self.publisher = ""
        self.relation = ""
        self.key_words = ""
        self.abstract = ""
        self.citation = ""
        self.citation_url = ""

    def to_list(self) -> List[str]:
        ret: List[str] = []
        ret.append(self.title)
        ret.append(self.authors)
        ret.append(self.teacher)
        ret.append(self.date)
        ret.append(self.publisher)
        ret.append(self.relation)
        ret.append(self.key_words)
        ret.append(self.abstract)
        ret.append(self.citation)
        ret.append(self.citation_url)
        return ret
