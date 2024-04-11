from flask import Flask,url_for,session,redirect,render_template
from authlib.integrations.flask_client import OAuth
import json
import requests
app=Flask(__name__)

appconf={
    "OAUTH2_CLIENT_ID":"118992035927-3aitg9ps830pro131mrdirsfl92mn0fe.apps.googleusercontent.com",
    "OAUTH2_CLIENT_SECRET":"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",
    "OAUTH2_META_URL":"https://accounts.google.com/.well-known/openid-configuration",
    "FLASK_SECRET":"stringsecret",
    "FLASK_PORT":5000
}
app.secret_key=appconf.get("FLASK_SECRET")
oauth=OAuth(app)
oauth.register("myApp",
               client_id=appconf.get("OAUTH2_CLIENT_ID"),
               client_secret=appconf.get( "OAUTH2_CLIENT_SECRET"),
               server_metadata_url=appconf.get("OAUTH2_META_URL"),
               client_kwargs={
                   "scope":"openid profile email https://www.googleapis.com/auth/user.birthday.read https://www.googleapis.com/auth/user.gender.read",
               }
               )

@app.route("/")
def home():
    return render_template("home.html",session=session.get("user"),pretty=json.dumps(session.get("user"), indent=4))
@app.route("/google-login")
def googlelogin():
    return oauth.myApp.authorize_redirect(redirect_uri=url_for("googleCallback",_external=True))

@app.route("/signin-google")
def googleCallback():
    token=oauth.myApp.authorize_access_token()
    persondataurl="https://people.googleapis.com/v1/people/me?personFields=genders,birthdays"

    persondata=requests.get(
        persondataurl,headers={
            "Authorization":f"Bearer {token['access_token']}"
        }
    ).json()
    token["persondata"]=persondata
    session["user"]=token

    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect(url_for("home"))


if __name__=='__main__':
    app.run(debug=True)

