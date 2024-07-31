from flask import Flask, render_template, request, Response, stream_with_context

import os
import subprocess
import json

app = Flask(__name__)


def execute_command(command):
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="utf-8",
        )
        for output_line in process.stdout:
            yield f"data: {json.dumps({'output': output_line})}\n\n"
    except subprocess.CalledProcessError as error:
        error_message = error.stderr.strip()
        yield f"data: {json.dumps({'output': error_message})}\n\n"
    finally:
        process.stdout.close()
        yield f"data: {json.dumps({'output': '[DONE]'})}\n\n"


@app.route("/")
def hello_world():
    # return "Hello, World!"

    # uname -a
    uname = subprocess.check_output(["uname", "-a"], encoding="utf-8")

    return render_template(
        "terminal.html", welcome_input="uname -a", welcome_output=uname
    )


# execute command
@app.route("/exec")
def exec():
    command = request.args.get("command")

    # event stream
    return Response(
        stream_with_context(execute_command(command)), mimetype="text/event-stream"
    )


if __name__ == "__main__":
    # port huggingface space
    app.run(host="0.0.0.0", port=7860, debug=True)
