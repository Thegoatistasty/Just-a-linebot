import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["nothing", "ask","joke","bad","friend", "love", "work","argument","trivial", "severe","fade","third", "nothird", "single", "progress","fixable", "notfixable"],
    transitions=[
        {
            "trigger": "advance",
            "source": "nothing",
            "dest": "ask",
            "conditions": "is_going_to_ask",
        },
        
        {
            "trigger": "advance",
            "source": "ask",
            "dest": "bad",
            "conditions": "is_going_to_bad",
        },
        {
            "trigger": "advance",
            "source": "ask",
            "dest": "nothing",
            "conditions": "is_going_to_nothing",
        },
#----------------------------------
        {
            "trigger": "advance",
            "source": "bad",
            "dest": "friend",
            "conditions": "is_going_to_friend",
        },
        {
            "trigger": "advance",
            "source": "bad",
            "dest": "love",
            "conditions": "is_going_to_love",
        },
        {
            "trigger": "advance",
            "source": "bad",
            "dest": "work",
            "conditions": "is_going_to_work",
        },
        {
            "trigger": "advance",
            "source": "love",
            "dest": "fade",
            "conditions": "is_going_to_fade",
        },
        {
            "trigger": "advance",
            "source": "fade",
            "dest": "third",
            "conditions": "is_going_to_third",
        },
        {
            "trigger": "advance",
            "source": "fade",
            "dest": "nothird",
            "conditions": "is_going_to_nothird",
        },
        {
            "trigger": "advance",
            "source": "love",
            "dest": "single",
            "conditions": "is_going_to_single",
        },
        {
            "trigger": "advance",
            "source": "work",
            "dest": "progress",
            "conditions": "is_going_to_progress",
        },
        {
            "trigger": "advance",
            "source": "progress",
            "dest": "fixable",
            "conditions": "is_going_to_fixable",
        },
        {
            "trigger": "advance",
            "source": "progress",
            "dest": "notfixable",
            "conditions": "is_going_to_notfixable",
        },
#-----------------------------------pool
        {
            "trigger": "advance",
            "source": ["friend","love"],
            "dest": "argument",
            "conditions": "is_going_to_argument",
        },
        {
            "trigger": "advance",
            "source": ["friend","work"],
            "dest": "jerk",
            "conditions": "is_going_to_jerk",
        },
        {
            "trigger": "advance",
            "source": "argument",
            "dest": "trivial",
            "conditions": "is_going_to_trivial",
        },
        {
            "trigger": "advance",
            "source": "argument",
            "dest": "severe",
            "conditions": "is_going_to_severe",
        },
        {"trigger": "advance", "source": ["bad","friend", "love", "work","argument"], "dest": "joke", "conditions": "is_going_to_joke"},
        {"trigger": "go_back", "source": ["joke","jerk","trivial", "severe", "nothird", "third", "single","fixable","notfixable"], "dest": "nothing"},
    ],
    initial="nothing",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Invalid option")

    return "OK"

@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")
def fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    fsm()
    app.run(host="0.0.0.0", port=port, debug=True)
