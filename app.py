from app import manager


if __name__ == '__main__':
    manager.run()  # You need to run the manager instance to be able to
    # perform migrations. You also now need to do `python app.py runserver`
    # to run the inbuilt flask server. Alternatively, `flask run` also works
    # as well and will load your environment variables in .flaskenv and .env
    # automatically. See: https://github.com/pallets/flask/pull/2416
