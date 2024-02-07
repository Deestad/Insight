import json
import sys
import time
import openai
import PySimpleGUI as SG
import os


class Initialize:

    def run(logging):
        TOKEN_FILE = "token.json"
        if os.path.isfile(TOKEN_FILE) and os.access(TOKEN_FILE, os.R_OK):
            logging.info("[Initializing...          ] Token detected...")
            with open(TOKEN_FILE, "r") as file:
                token_data = json.load(file)
                ai_token = token_data.get("openaitoken")
                openai.api_key = ai_token
        else:
            logging.warning("[Initializing...          ] Could not find Token...")
            token = SG.PopupGetText("Enter your OpenAI API key.", title="Configuration")
            data = {
                'openaitoken': token,
            }
            with open(TOKEN_FILE, "w") as file:
                json.dump(data, file)
            SG.Popup("Restart Insight.")
            sys.exit()
