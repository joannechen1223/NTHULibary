# Introduction
此專案透過Python套件selenium、bs4網頁爬蟲，下載清華大學論文資料。
# Installation
1. 安裝pipenv
安裝方式可參考：https://pypi.org/project/pipenv/
2. 在此目錄底下執行下列指令，進入虛擬環境並安裝套件
    pipenv shell
    pipenv install
3. 在此目錄底下執行指令
    * 從教授論文目錄下載論文標題、提名網址等
        make start-download-list
    * 從論文資料頁面下載論文標題、摘要等資訊
    make start-download-info
    * 下載論文目錄中的超連結pdf
    make start-download-pdf
    * 依序執行上述三項
    make start
    * 清除資料
    將上面指令的 make 換成 clean 可清除資料
    ex. make clean