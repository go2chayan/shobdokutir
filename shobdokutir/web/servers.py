import json
from flask import Flask, request


def run_parrot_server(host_name: str = '0.0.0.0', port_num: int = 6976) -> None:
    """
    Run a parrot server in a specific port. A parrot server says the same thing that it receives.
    """
    app = Flask(__name__)

    @app.route('/')
    def index() -> str:
        json_str = request.args.get("message")
        font_name = request.args.get("font")
        font_size = request.args.get("size")

        message = json.loads(json_str)

        if font_name:
            font_name_text = f"font-family: {font_name};"
        else:
            font_name_text = ""

        if font_size:
            font_size_text = f"font-size: {font_size}px;"
        else:
            font_size_text = ""

        if font_name or font_size:
            style_text = f"style = \"{font_name_text} {font_size_text}\""
        else:
            style_text = ""

        formatted_text = f"<html><body><span {style_text}>{message}</span></body></html>"

        return formatted_text

    app.run(host=host_name, port=port_num, debug=False)
