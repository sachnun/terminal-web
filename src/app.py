from flask import Flask, render_template, request, Response, stream_with_context

import subprocess
import json
import os
import time

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
            if not "/bin/sh:" in pwd:
                yield f"data: {json.dumps({'pwd': pwd})}\n\n"
            return

        output = ""
        start_time = time.time()
        for line in process(command, pwd):
            output += line
            current_time = time.time()
            if current_time - start_time >= 0.3:
                yield f"data: {json.dumps({'output': output})}\n\n"
                output = ""
                start_time = current_time
        if output:
            yield f"data: {json.dumps({'output': output})}\n\n"

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
