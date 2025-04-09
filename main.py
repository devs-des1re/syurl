from flask import Flask
from flask import render_template, request, redirect, url_for

import os
from dotenv import load_dotenv

import sqldb

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        long_link = request.form["url-input"]

        if long_link.strip() != '':
            code = sqldb.create_url(long_link)
            return redirect(url_for(f"shortened", code=code), code=302)
        else:
            return render_template("invalid_link.html")
    else:
        return render_template("index.html")
    
@app.route("/about-us")
def about_us():
    return render_template("about_us.html")

@app.route("/donate")
def donate():
    return render_template("donate.html")

@app.route("/github")
def github():
    return render_template("github.html")

@app.route("/shortened")
def shortened():
    code = request.args.get("code", None)

    if not code:
        return render_template("error404.html")
    else:
        return render_template("shortened_link.html", link=code)
    
@app.route("/terms-of-service")
def tos():
    return render_template("tos.html")

@app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy_policy.html")

@app.route("/link/<string:link_id>")
def short_link(link_id):
    url = sqldb.get_url(link_id)

    if url:
        return render_template("short_link.html", link=url)
    else:
        return render_template("invalid_link.html")
    
@app.route("/api/shorten")
def api_shorten():
    long_link = request.args.get("long_link", None)
    if long_link != None:
        code = sqldb.create_url(long_link)
        return {
            "code": 201, ""
            "link": f"https://syurl.net/link/{code}", 
            "link_id": code
        }
    else:
        return {
            "code": 400, 
            "error": "Link not provided"
        }

@app.errorhandler(404)
def error_404(error):
    return render_template("error404.html"), 404  

if __name__ == "__main__":
    load_dotenv()
    host = os.getenv("HOST")
    port = os.getenv("PORT")

    app.run(host=host, port=port, debug=True)