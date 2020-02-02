import sys
import flask
from flask import Flask, request
import json
import pymysql
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--mysql_host", type=str)
parser.add_argument("--mysql_user", type=str)
parser.add_argument("--mysql_password", type=str)
parser.add_argument("--mysql_database", type=str)
args = parser.parse_args()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def test():
    mysql_config = {}
    mysql_config["host"] = args.mysql_host
    mysql_config["user"] = args.mysql_user
    mysql_config["password"] = args.mysql_password
    mysql_config["database"] = args.mysql_database

    # connect the SQL server to fetch data
    db = pymysql.connect(**mysql_config)
    cursor = db.cursor()
    query = ("SELECT tbl1_title, tbl1_author FROM tbl1 WHERE tbl1_id=3")
    cursor.execute(query)
    data = {}
    for (title, author) in cursor:
        data["title"] = title
        data["author"] = author
    cursor.close()
    db.close()

    return json.dumps(data)


def main():
    port = 8888
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()