# To-Do App
## Built in Flask using sqlite3

So, to set this up, just pull the repo down, then create a virtualenv (I prefer `virtualenvwrapper`)
then you have to run (inside the virtualenv):
```
(venv) $ pip install -R requirements.txt
(venv) $ flask db init
	...
(venv) $ flask db migrate -m "initialize database using models.py"
	...
(venv) $ flask db upgrade
	...
```
and that should create the `app.db` file in the root directory of the project.

You probably also want to set shell environment variables:
`$ export FLASK_APP=app.py` and optionally
`$ export FLASK_DEBUG=1`

now just type `(venv) $ flask run`, and the server should be running on 127.0.0.1:5000!
