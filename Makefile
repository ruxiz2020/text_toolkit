.venv/bin/pip:
	virtualenv -p /usr/bin/python3 env

install:
	env/bin/pip install nltk
	env/bin/python -m nltk.downloader all
	env/bin/pip install -Ur requirements.txt
