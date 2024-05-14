
start-p1:
	PYTHONPATH=./ poetry run python3 ./project1/main.py

start-p1-scrape:
	PYTHONPATH=./ poetry run python3 ./project1/scrape.py

start-p3:
	PYTHONPATH=./ poetry run python3 ./project3/main.py

start-p3-cp-sat:
	PYTHONPATH=./ poetry run python3 ./project3/cpsat.py
	