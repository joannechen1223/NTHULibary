start:
	make start-download-list
	make start-download-info
	make start-download-pdf
start-download-list:
	mkdir ./NTHU1
	pipenv run python3 ./main.py list
start-download-info:
	mkdir ./NTHU2
	pipenv run python3 ./main.py info
start-download-pdf:
	mkdir ./NTHU3
	pipenv runpython3 ./main.py pdf

clean:
	rm -rf ./NTHU*
clean-download-list:
	rm -rf ./NTHU1/
clean-download-info:
	rm -rf ./NTHU2/
clean-download-pdf:
	rm -rf ./NTHU3/