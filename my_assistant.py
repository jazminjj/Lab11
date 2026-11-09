# my_assistant.py
# Author: Jazmin Joseph

HANDOFF_WORDS = ["allerg", "gluten", "dairy", "ingredient"]

SAFE_REPLY = (
    "I'm not sure how to help with that. I can tell you the price of a menu item."
)


class MenuHelper:
    def __init__(self, name, instructions, menu_board, model):
        """Set up one helper with its own name, instructions, tool, and history."""
        self.name = name
        self.instructions = instructions
        self.menu_board = menu_board
        self.model = model
        self.history = []

    def respond(self, user_message):
        """Record the user's message, choose a reply, record it, and return it."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        """Choose a reply with keyword rules. This is the mock part."""
        text = user_message.lower()
        if self.needs_human(text):
            return "I can't help with that allergy or ingredient question. I'm passing you to a human agent."
        if "price" in text or "cost" in text or "how much" in text:
            return self.price_reply(user_message)
        if "menu" in text:
            return f"Our menu: {self.menu_board.list_items()}"
        return self.model_reply()

    def model_reply(self):
        """Ask the model for a reply. Give a safe answer if the model has non."""
        reply = self.model.reply(self.instructions, self.history)
        if reply is None:
            return "Sorry, I cant answer that right now. Please try again in a moment."
        return reply

    def needs_human(self, text):
        """Return true if the message is about something a person must handle."""
        for word in HANDOFF_WORDS:
            if word in text:
                return True
        return False

    def price_reply(self, user_message):
        """Use the menu board to answer a question about the price of an item."""
        item = self.menu_board.find_item(user_message)
        if item is None:
            return "Which item? Type menu to see what we have."
        price = self.menu_board.price_for(item)
        return f"The {item} costs ${price:.2f}."
