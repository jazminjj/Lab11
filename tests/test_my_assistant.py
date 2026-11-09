from mock_model import MockModel
from my_assistant import MenuHelper
from my_tool import MenuBoard


class SilentModel:
    """a model that never has an answer. it stands in for Ollama being switched off."""

    def reply(self, instructions, history):
        return None


def make_bot():
    """Build a fresh chat bot with its own tool for each test."""
    menu = {"latte": 4.50, "croissant": 2.75}
    return MenuHelper("Mocha", "Be friendly", MenuBoard(menu), MockModel())


def make_bot_with_silent_model():
    """Build a bot whose model never answers."""
    menu = {"latte": 4.50, "croissant": 2.75}
    return MenuHelper("Mocha", "Be friendly.", MenuBoard(menu), SilentModel())


def test_unknown_request_gets_a_safe_reply():
    bot = make_bot_with_silent_model()
    assert "try again" in bot.respond("Do you have wifi?")


def test_price_question_uses_the_tool():
    bot = make_bot()
    assert bot.respond("How much is a latte?") == "The latte costs $4.50."


def test_price_question_without_an_item_ask_for_one():
    bot = make_bot()
    assert "Which item" in bot.respond("How much is that?")


def test_unknown_item_does_not_get_a_made_up_price():
    bot = make_bot()
    assert "$" not in bot.respond("How much is a pizza?")


def test_allergy_question_goes_to_a_human():
    bot = make_bot()
    assert "human" in bot.respond("Does the croissant have gluten?")


def test_history_grows_by_two_each_turn():
    bot = make_bot()
    bot.respond("Hello")
    bot.respond("menu")
    assert len(bot.history) == 4


def test_other_messages_go_to_the_model():
    bot = make_bot()
    assert bot.respond("hello") == "Hello! How can I help you today?"


def test_price_rule_does_not_need_the_model():
    bot = make_bot_with_silent_model()
    assert "$4.50" in bot.respond("How much is a latte?")


def test_handoff_rule_does_not_need_the_model():
    bot = make_bot_with_silent_model()
    assert "human agent" in bot.respond("Is the croissant gluten free?")
