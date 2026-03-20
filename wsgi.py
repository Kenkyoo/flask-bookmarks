from flaskr import create_app

app = create_app()

waitress-serve --host=0.0.0.0 --port=10000 wsgi:app

waitress
