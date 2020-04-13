from flask import Flask, jsonify, send_from_directory, request
from werkzeug.exceptions import BadRequest, HTTPException
from pathlib import Path
from urllib.parse import quote


ROUTE_DIR = "."

app = Flask("py-gexporter", static_folder=None)
app.config.from_object(__name__)


def create_json_index(root: Path):
    pass


@app.errorhandler(HTTPException)
def json_error(e: HTTPException):
    response = jsonify({"error": e.description})
    response.status_code = e.code
    return response


# Looking at gimporter's gimporterApp.mc and gexporter's WebServer.java:
# type = GPX|FIT
#   dir: filter the result by GPX/FIT suffix
# short:
#   0 - url is the full URL
#   1 - url is just the URL-encoded filename
# longname:
#   0 - track is first 15 characters of filename without suffix
#   1 - track is full filename including suffix
# _But_ gimporterApp _always_ sets both params to 1, so we'll ignore them


@app.route("/dir.json")
def dir_json():
    files = []
    type = request.args.get("type")
    if type == "FIT":
        files = Path(app.config["ROUTE_DIR"]).glob("*.fit")
    elif type == "GPX":
        files = Path(app.config["ROUTE_DIR"]).glob("*.gpx")
    else:
        raise BadRequest("Bad type {}".format(type))

    results = [
        {"url": quote(file.name, encoding="utf-8"), "track": file.name}
        for file in files
    ]

    return jsonify(results)


@app.route("/<path:filename>")
def route_file(filename):
    mimetype = None
    type = request.args.get("type")
    if type == "FIT":
        mimetype = "application/fit"
    elif type == "GPX":
        mimetype = "application/gpx+xml"
    else:
        raise BadRequest("Bad type {}".format(type))

    return send_from_directory(app.config["ROUTE_DIR"], filename, mimetype=mimetype)


if __name__ == "__main__":
    app.run(port=22222)
