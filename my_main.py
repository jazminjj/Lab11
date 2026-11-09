# my_main.py
# Author: Jazmin Joseph

from my_assistant import MenuHelper
from my_tool import MenuBoard
from ollama_model import OllamaModel

MODEL_NAME = "granite4.1:3b"

INSTRUCTIONS = """You are Mocha, the assistant for Sunrise Cafe.
Answer in one short sentence.
We are open 7 am to 3 pm, Monday through Saturday.
We are located at 120 Main Street and we have free wifi.
Only state facts that appear in these instructions.
If you do not know, say you do not know and offer to pass the customer to a human agent."""

MENU = {
    "latte": 4.50,
    "cappuccino": 4.25,
    "iced coffee": 3.75,
    "blueberry muffin": 3.00,
    "croissant": 2.75,
}

menu_board = MenuBoard(MENU)
model = OllamaModel(MODEL_NAME)
bot = MenuHelper("Mocha", INSTRUCTIONS, menu_board, model)

print("Type a message, or type quit to stop.")
user_message = input("You: ")
while user_message != "quit":
    print(f"{bot.name}: {bot.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(bot.history)}")
