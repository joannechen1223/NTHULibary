import concurrent.futures
import os
from os.path import isdir, join


class DownloadPdfs(object):

    _MAX_WORDERS = 1

    def __init__(
        self,
        input_dir,
        target_dir,
        pdf_service
    ):
        self._input_dir = input_dir
        self._target_dir = target_dir
        self._pdf_service = pdf_service

    def execute(self):
        departments = self._find_all_departments()
        with concurrent.futures.ThreadPoolExecutor(
           max_workers=self._MAX_WORDERS) as executor:
            for d in departments:
                files = os.listdir(self._input_dir + d)
                for filename in files:
                    professor_dir_name = self._target_dir + d + \
                        "/" + filename[:-5]
                    if not os.path.exists(professor_dir_name):
                        os.mkdir(professor_dir_name)
                    executor.submit(
                        self._pdf_service.download_pdfs,
                        self._input_dir + d + "/" + filename,
                        professor_dir_name
                    )

    def _find_all_departments(self):
        departments = []
        dirs = os.listdir(self._input_dir)
        for ddir in dirs:
            fullpath = join(self._input_dir, ddir)
            if isdir(fullpath) and not ddir.startswith('.') and \
               not os.path.exists(self._target_dir + ddir):
                os.mkdir(self._target_dir + ddir)
                departments.append(ddir)
        return departments
