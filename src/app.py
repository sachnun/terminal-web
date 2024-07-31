from flask import Flask, render_template, request, Response, stream_with_context

import subprocess
import json
import os

app = Flask(__name__)


def execute_command(command: str, pwd: str):
    def process(command: str, pwd: str):
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="utf-8",
            cwd=pwd,
        )
        yield from process.stdout

    try:

        # have cd command so change pwd
        if command.startswith("cd") and "&&" not in command:
            pwd = next(process(command + " && pwd", pwd)).strip()
            yield f"data: {json.dumps({'output': pwd})}\n\n"
            if not "not found" in pwd:
                yield f"data: {json.dumps({'pwd': pwd})}\n\n"
            return

        for output_line in process(command, pwd):
            yield f"data: {json.dumps({'output': output_line})}\n\n"
    except subprocess.CalledProcessError as error:
        error_message = error.stderr.strip()
        yield f"data: {json.dumps({'output': error_message})}\n\n"
    finally:
        yield f"data: {json.dumps({'output': '[DONE]'})}\n\n"


@app.route("/")
def hello_world():
    # return "Hello, World!"

    # uname -a
    uname = subprocess.check_output(["uname", "-a"], encoding="utf-8")

    return render_template(
        "terminal.html", welcome_input="uname -a", welcome_output=uname, pwd="/root"
    )


# execute command
@app.route("/exec")
def exec():
    command = request.args.get("command")
    pwd = request.args.get("pwd")

    # event stream
    return Response(
        stream_with_context(execute_command(command, pwd)), mimetype="text/event-stream"
    )


# ping
@app.route("/ping")
def ping():
    # 204
    return Response(status=204)


if __name__ == "__main__":
    # port huggingface space
    app.run(host="0.0.0.0", port=7860, debug=True)
