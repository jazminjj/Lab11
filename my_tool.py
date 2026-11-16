# my_tool.py
# Jazmin Joseph


class MenuBoard:
    """A tool that knows about the menu. It knows nothing about chatting."""

    def __init__(self, menu):
        """Store the menu this tool can look up, and start with no orders."""
        self.menu = menu
        self.orders = []

    def find_item(self, text):
        """Return the first known menu item mentioned in text, or None."""
        for item in self.menu:
            if item in text.lower():
                return item
        return None

    def price_for(self, item):
        """Return the price of one menu item, or None if unknown."""
        if item in self.menu:
            return self.menu[item]
        return None

    def list_items(self):
        """Return a list of all menu items as one comma-separated string."""
        return ", ".join(self.menu)

    def check_price(self, item):
        """Look up the price of one menu item.

        Args:
            item: The menu item name, like latte.
        """
        found = self.find_item(item)
        if found is None:
            return "That item was not found on the menu."
        return f"The {found} costs ${self.price_for(found):.2f}."

    def add_order(self, item, customer):
        """Record one approved order. Only an approval calls this."""
        self.orders.append({"item": item, "customer": customer})
