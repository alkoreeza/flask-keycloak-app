from flask import Flask, redirect, request, session, render_template
from keycloak import KeycloakOpenID
import json


app = Flask(__name__)
app.secret_key = "supersecretkey123"


# Load Keycloak config
with open("keycloak.json") as f:
config = json.load(f)


keycloak_openid = KeycloakOpenID(
server_url=config["auth-server-url"],
client_id=config["resource"],
realm_name=config["realm"],
verify=False,
)


@app.route("/")
def home():
if "token" not in session:
return redirect("/login")
return render_template("index.html", user=session.get("user"))


@app.route("/login")
def login():
auth_url = keycloak_openid.auth_url(redirect_uri="http://192.168.0.19:5000/callback")
return redirect(auth_url)


@app.route("/callback")
def callback():
code = request.args.get("code")
token = keycloak_openid.token("http://192.168.0.19:5000/callback", code)
userinfo = keycloak_openid.userinfo(token["access_token"])


session["token"] = token
session["user"] = userinfo


return redirect("/")


@app.route("/logout")
def logout():
session.clear()
return "Logged out"


if __name__ == "__main__":
app.run(host="0.0.0.0", port=5000)