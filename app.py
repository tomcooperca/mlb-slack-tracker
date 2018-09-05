from slack.token import Token
from flask import Flask, send_from_directory, request
from celery import Celery
app = Flask(__name__, static_url_path='')
# app.config.update(
#     CELERY_BROKER_URL='redis://localhost:6379',
#     CELERY_RESULT_BACKEND='redis://localhost:6379'
# )
# celery = make_celery(app)

@app.route("/")
def hello():
    return app.send_static_file("slack_button.html")

@app.route("/authorize")
def authorize():
    try:
        t = Token(request.args.get('code'),
            os.environ['SLACK_CLIENT_ID'],
            os.environ['SLACK_CLIENT_SECRET'])
    except KeyError:
        print("No auth code")
    else:
        return t.generate_token()
    return "Didn't generate token"


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
