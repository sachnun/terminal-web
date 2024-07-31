from flask import Flask, render_template, request, Response

import os
import subprocess

app = Flask(__name__)


def execute_command(command):
    try:
        result = subprocess.check_output(
            command, shell=True, stderr=subprocess.STDOUT
        ).decode("utf-8")
    except subprocess.CalledProcessError as e:
        result = e.output.decode("utf-8")

    return result


@app.route("/")
def hello_world():
    # return "Hello, World!"

    # uname -a
    uname = execute_command("uname -a")

    return render_template("terminal.html", welcome=uname)


# execute command
@app.route("/exec", methods=["POST"])
def exec():
    command = request.form["command"]

    return Response(execute_command(command), mimetype="text/plain")


if __name__ == "__main__":
    # port huggingface space
    app.run(host="0.0.0.0", port=7860, debug=True)
