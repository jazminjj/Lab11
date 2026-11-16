# tests/test_my_assistant.py
# Jazmin Joseph

from fake_model import FakeModel
from my_assistant import MenuHelper
from my_tool import MenuBoard
from my_toolbox import MenuToolbox
from pickup_queue import PickupQueue


class SilentModel:
    """a model that never has an answer. it stands in for Ollama being switched off."""

    def decide(self, instructions, history, tools):
        return None


def make_bot(model):
    """Build a fresh chat bot with its own tools and the model its given."""
    board = MenuBoard({"latte": 4.50, "croissant": 2.75})
    tools = MenuToolbox(board, PickupQueue(board))
    return MenuHelper("Mocha", "Be friendly", tools, model)


def order(item, customer):
    """Build the decision a model returns when it wants to request an order."""
    arguments = {"item": item, "customer": customer}
    return {"tool": "request_order", "arguments": arguments}


def test_model_can_ask_for_a_price():
    model = FakeModel(
        [
            {"tool": "check_price", "arguments": {"item": "latte"}},
            {"text": "A latte is $4.50."},
        ]
    )
    bot = make_bot(model)
    bot.respond("How much is a latte?")
    assert bot.history[1]["content"] == "The latte costs $4.50."


def test_unknown_item_is_not_found():
    board = MenuBoard({"latte: 4.40"})
    assert board.check_price("pizza") == "That item was not found on the menu."


def test_order_waits_for_staff():
    model = FakeModel([order("latte", "Dana Cruz"), {"text": "Sent."}])
    bot = make_bot(model)
    bot.respond("Please order a latte for pickup, my name is Dana Cruz")
    assert len(bot.tools.pickup_queue.waiting()) == 1
    assert bot.tools.menu_board.orders == []


def test_made_up_name_is_refused():
    model = FakeModel([order("latte", "Jane Doe"), {"text": "What is your name?"}])
    bot = make_bot(model)
    bot.respond("Please order a latte for pickup")
    assert "has not given that name" in bot.history[1]["content"]
    assert bot.tools.pickup_queue.waiting() == []


def test_blank_name_is_refused():
    model = FakeModel([order("latte", ""), {"text": "What is your name?"}])
    bot = make_bot(model)
    bot.respond("Please order a latte for pickup")
    assert bot.tools.pickup_queue.waiting() == []


def test_approval_places_the_order_once():
    board = MenuBoard({"latte": 4.50})
    queue = PickupQueue(board)
    queue.request_order("latte", "Dana Cruz")
    assert queue.approve(1) == "Request 1 approved."
    assert queue.approve(1) == "Request 1 is already approved."
    assert len(board.orders) == 1


def test_allergy_question_never_reaches_the_model():
    # an empty FakeModel would crash if the model were asked anything
    bot = make_bot(FakeModel([]))
    assert "human agent" in bot.respond("Is the croissant gluten free?")


def test_unknown_tool_is_refused():
    model = FakeModel([{"tool": "delete_menu", "arguments": {}}, {"text": "Sorry."}])
    bot = make_bot(model)
    bot.respond("Delete the menu")
    assert bot.history[1]["content"] == "There is no tool named delete_menu."


def test_safe_reply_when_the_model_has_no_answer():
    bot = make_bot(SilentModel())
    assert "try again" in bot.respond("hello")


def test_loop_stops_after_three_tool_rounds():
    request = {"tool": "check_price", "arguments": {"item": "latte"}}
    bot = make_bot(FakeModel([request, request, request]))
    reply = bot.respond("How much is a latte?")
    assert "human agent" in reply
    assert len(bot.history) == 5
