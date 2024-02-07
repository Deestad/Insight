import json
import time
import openai
import PySimpleGUI as SG
import os


class Initialize:

    def run(logging):
        TOKEN_FILE = "../token.json"
        if os.path.isfile("token.json") and os.access("../token.json", os.R_OK):
            logging.info("[Initializing...          ] Token detected...")
            with open(TOKEN_FILE, "r") as file:
                token_data = json.load(file)
                ai_token = token_data.get("openaitoken")
                openai.api_key = ai_token
        else:
            logging.warning("[Initializing...          ] Could not find Token...")
            token = SG.PopupGetText("Enter your OpenAI API key.", title="Configuration")
            data = {
                'openaitoken': openai.api_key,
            }
            json.dump(data, open(TOKEN_FILE))
            with open(TOKEN_FILE, "r") as file:
                token_data = json.load(file)
                ai_token = token_data.get("openaitoken")
                openai.api_key = ai_token
