# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from datetime import datetime

import logging
import requests
import json
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

logger = logging.getLogger(__name__)

class ApiAction(Action):
	def name(self) -> Text:
		return "action_match_news"

	async def run(self,dispatcher,tracker: Tracker,domain: "DomaindDict",) -> List[Dict[Text, Any]]:
		API_URL = "https://cricapi.com/api/"
		API_KEY = "IrL45NRdSRZFI6e43mtUD8k3tK52"
		res = requests.get(API_URL + "matches" + "?apikey=" + API_KEY)
		if res.status_code == 200:
			data = res.json()["matches"]
			recent_match = data[0]
			upcoming_match = data[1]
			upcoming_match["date"] = datetime.strptime(upcoming_match["date"], "%Y-%m-%dT%H:%M:%S.%fZ")
			next_date = upcoming_match["date"].strftime("%d %B %Y")

			out_message = "Here some IPL quick info:\n1.The match between {} and {} was recently held.".format(recent_match["team-1"], recent_match["team-2"])

			dispatcher.utter_message(out_message)

			out_message = "2.The next match is {} vs {} on {}".format(upcoming_match["team-1"], upcoming_match["team-2"], next_date)

			dispatcher.utter_message(out_message)

		return []
