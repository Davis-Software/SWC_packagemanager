import os
import sys
import json
import uuid
from server_files import watchdog_component

from server_files.code_containers import js_socketio, javascript, html_base

from flask import Flask, render_template, make_response
from flask_socketio import SocketIO


working_dir = os.path.abspath("")

config_file = "conf.json"
templates_folder = "templates"
static_folder = "static"


def ask_content(*values: tuple or str):
    def convert(val, default):
        if val == "":
            return None
        if type(val) == type(default):
            return val
        elif type(default) == bool:
            return val == "True"
        elif type(default) == str:
            return str(val)
        elif type(default) == int:
            return int(val)
        else:
            print(f"Error: Value must be of type {type(default).__name__}")
            exit()
    content = {}
    for value in values:
        if type(value) == tuple:
            print(f"Enter value for '{value[0]}' or leave default at '{value[1]}'")
            alt = convert(input(f"{value[0]}: [Blank for default] >"), value[1])
            if alt is not None:
                content[value[0]] = alt
                print(f"Set value '{value[0]}' to '{alt}'")
            else:
                content[value[0]] = value[1]
                print(f"Used default '{value[1]}' for value '{value[0]}'")
        elif type(value) == str:
            print(f"Set value for '{value}'")
            alt = input(f"{value} >")
            if alt == "" or type(alt) != str:
                print("Error: Value must not be None and of type string")
                exit(1)
            else:
                content[value] = alt
        else:
            print(f"Error: Value must be of type 'tuple' with format '(name: str, default: bool or str or int)' or 'str', but it was '{[type(value).__name__]}'")
    return content


if not os.path.exists(os.path.join(working_dir, config_file)):
    def iterate_template(path_add, template):
        for part in template:
            path = os.path.join(working_dir, path_add, part["name"])
            if not os.path.exists(path):
                if part["type"] == "folder":
                    os.makedirs(path)
                    iterate_template(path, part["content"])
                elif part["type"] == "file":
                    filetype = part["name"].split(".")[-1]
                    with open(path, "w") as f:
                        if filetype == "json":
                            f.write(json.dumps(part["content"]))
                        else:
                            f.write(part["content"])
                else:
                    print(f"Error: Type value can only be 'file' or 'folder', not '{part['type']}'")
                    exit(1)

    arguments = sys.argv[1:]
    if len(arguments) == 1 and arguments[0] in ["-h", "-help", "--h", "--help"]:
        print("-t <templatefile.json>  Custom builder template file")
        exit(0)
    if len(arguments) == 2 and arguments[0] in ["-t", "-template", "--t", "--template"] and os.path.exists(os.path.join(working_dir, arguments[1])):
        with open(os.path.join(working_dir, arguments[1]), "r") as f:
            iterate_template("", json.loads(f.read()))
    else:
        layout_template = [
            {
                "name": templates_folder,
                "type": "folder",
                "content": [
                    {
                        "name": "index.html",
                        "type": "file",
                        "content": html_base
                    }
                ]
            },
            {
                "name": static_folder,
                "type": "folder",
                "content": [
                    {
                        "name": "base",
                        "type": "folder",
                        "content": [
                            {
                                "name": "js_base.js",
                                "type": "file",
                                "content": javascript
                            },
                            {
                                "name": "socket.io.js",
                                "type": "file",
                                "content": js_socketio
                            }
                        ]
                    },
                    {
                        "name": "script.js",
                        "type": "file",
                        "content": "//your js goes here"
                    }
                ]
            },
            {
                "name": config_file,
                "type": "file",
                "content": ask_content(
                    ("host", "0.0.0.0"),
                    ("port", "80")
                )
            }
        ]
        iterate_template("", layout_template)


with open(os.path.join(working_dir, config_file), "r") as f:
    settings = json.loads(f.read())


app = Flask(
    __name__,
    static_folder=static_folder,
    template_folder=templates_folder
)
app.config['SECRET_KEY'] = str(uuid.uuid4())
socketio = SocketIO(app)


@app.route("/", defaults={"path": "index.html"})
@app.route("/<path>")
def routing(path):
    if os.path.exists(os.path.join(working_dir, "templates", path)):
        return render_template(path)
    return make_response("404 Not found", 404)


@app.errorhandler(Exception)
def error(err):
    return err


def emit_reload(e):
    print(f"Changes in {e.src_path}! Reloading all clients...")
    socketio.emit("reload")


def main():
    try:
        watchdog_component.run_daemon(working_dir, emit_reload)
        socketio.run(
            app,
            settings["host"],
            settings["port"],
            debug=True
        )
    except PermissionError:
        print(f"Error: Port '{settings['port']}' already in use!")


if __name__ == "__main__":
    main()
