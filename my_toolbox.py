# my_toolbox.py
# Jazmin Joseph


class MenuToolbox:
    """Every tool request from the model comes through here and is checked."""

    def __init__(self, menu_board, pickup_queue):
        """Hold the tools the menu is allowed to ask for."""
        self.menu_board = menu_board
        self.pickup_queue = pickup_queue

    def tool_list(self):
        """Return the tools the model may ask for. They are not called here."""
        return [
            self.menu_board.check_price,
            self.pickup_queue.request_order,
        ]

    def run(self, name, arguments, history):
        """Check one tool request. Run the tool only if every check passes."""
        if name == "check_price":
            item = self.clean(arguments, "item")
            if item == "":
                return "The item is missing. Ask the customer which item."
            return self.menu_board.check_price(item)
        if name == "request_order":
            item = self.clean(arguments, "item")
            customer = self.clean(arguments, "customer")
            if item == "" or customer == "":
                return "The item annd the customer's name are both needed."
            if not self.customer_said(history, item):
                return "The customer has not given that name. Ask them for it."
            if not self.customer_said(history, customer):
                return "The customer has not given that name. Ask them for it."
            return self.pickup_queue.request_order(item, customer)
        return f"There is no tool named {name}."

    def clean(self, arguments, key):
        """Return one argument as tect without extra spaces, or "" if it is missing."""
        return str(arguments.get(key, "")).strip()

    def customer_said(self, history, text):
        """Return True if text appears in a message the customer typed."""
        for message in history:
            if message["role"] == "user" and text.lower() in message["content"].lower():
                return True
        return False
