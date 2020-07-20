# text_toolkit




## How to run reporting tool


```bash
virtualenv -p python3 env
source env/bin/activate
```

Install the requirements:

```bash
env/bin/pip install -r requirements.txt

env/bin/pip install . -U --force-reinstall --no-deps
```
Run the app:

```bash
env/bin/python text_toolkit/reporting/app.py
```
Open a browser at http://127.0.0.1:8050


## deploying it on Heroku

```bash
heroku create  text-toolkit

git remote add heroku  text-toolkit

```
