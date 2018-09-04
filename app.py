from flask import Flask, send_from_directory
app = Flask(__name__, static_url_path='')

@app.route("/")
def hello():
    return app.send_static_file("slack_button.html")

@app.route("/authorize")
def authorize():
    #TODO Cache this user's auth code, generate a token and send message in Slack to confirm
    return "Authorized"
