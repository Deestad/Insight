import json
import sys
import time
import openai
import easygui
import os
import logging

class Initialize:

    def run(self):
        # Logging
        LOG_FILE = '../Insight.log'
        if os.path.isfile(LOG_FILE) and os.access(LOG_FILE, os.R_OK):
            os.remove('Insight.log')
        logging.basicConfig(filename='Insight.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s', force=True)

        TOKEN_FILE = "token.json"
        if os.path.isfile(TOKEN_FILE) and os.access(TOKEN_FILE, os.R_OK):
            logging.info("[Initializing...          ] Token detected...")
            with open(TOKEN_FILE, "r") as file:
                token_data = json.load(file)
                ai_token = token_data.get("openaitoken")
                openai.api_key = ai_token
        else:
            logging.warning("[Initializing...          ] Could not find Token...")

            #token = SG.PopupGetText("Enter your OpenAI API key.", title="Configuration")
            title = "Insight configuration processus"
            msg = "Insert your OpenAI token."
            token = easygui.enterbox(msg,title)
            data = {
                'openaitoken': token,
            }
            with open(TOKEN_FILE, "w") as file:
                json.dump(data, file)
            sys.exit()
