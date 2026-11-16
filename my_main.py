# my_main.py
# Author: Jazmin Joseph

from my_assistant import MenuHelper
from my_tool import MenuBoard
from my_toolbox import MenuToolbox
from ollama_model import OllamaModel
from pickup_queue import PickupQueue

MODEL_NAME = "granite4.1:3b"

INSTRUCTIONS = """You are Mocha, the assistant for Sunrise Cafe.
Answer in one short sentence.
If the customer only says hello, greet them and ask how you can help.
We are open 7 am to 3 pm, Monday through Saturday.
We sell latte, cappuccino, iced coffee, blueberry muffin, and croissant.
Prices come from the price tool.
To request a pickup order you need the item and the customers name. Never guess a name.
Only state facts that appear in these instructions or in tool results.
If you do not know, say you do not know and offer to pass the customer to a staff member."""

MENU = {
    "latte": 4.50,
    "cappuccino": 4.25,
    "iced coffee": 3.75,
    "blueberry muffin": 3.00,
    "croissant": 2.75,
}

menu_board = MenuBoard(MENU)
pickup_queue = PickupQueue(menu_board)
tools = MenuToolbox(menu_board, pickup_queue)
model = OllamaModel(MODEL_NAME)
bot = MenuHelper("Mocha", INSTRUCTIONS, tools, model)

print("Type a message, or type quit to stop.")
user_message = input("You: ")
while user_message != "quit":
    print(f"{bot.name}: {bot.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(bot.history)}")

print("Staff review")
for request in pickup_queue.waiting():
    number = request["number"]
    print(f"Request {number}: {request['customer']}, {request['item']}")
    answer = input("Approve? yes or no")
    if answer == "yes":
        print(pickup_queue.approve(number))
    else:
        print(pickup_queue.reject(number))

print(f"Orders: {len(menu_board.orders)}")
