# pickup_queue.py
# Jazmin Joseph


class PickupQueue:
    """Orders waiting for staff to approve. Nothing is ordered until they approve."""

    def __init__(self, menu_board):
        """Start with no requests. Approved orders go into the menu board."""
        self.menu_board = menu_board
        self.requests = []

    def request_order(self, item, customer):
        """Ask staff to place a pickup order. Staff must approve it.

        Args:
            item: The menu item name, like latte.
            customer: The customer's name for the pickup order.
        """
        # refuse items that arent on the menu instead of filing them
        found = self.menu_board.find_item(item)
        if found is None:
            return "That item was not found on the menu."
        number = len(self.requests) + 1
        request = {
            "number": number,
            "item": found,
            "customer": customer,
            "status": "waiting",
        }
        self.requests.append(request)
        return f"Request {number} was sent to staff. Nothing is ordered yet."

    def waiting(self):
        """Return the requests that are still waiting for a decision."""
        result = []
        for request in self.requests:
            if request["status"] == "waiting":
                result.append(request)
        return result

    def find(self, number):
        """Return the request with this number, or None."""
        for request in self.requests:
            if request["number"] == number:
                return request
        return None

    def approve(self, number):
        """Approve one waiting request and place the order."""
        request = self.find(number)
        if request is None:
            return f"There is no request {number}."
        # a request thats already approved or rejected changes nothing
        if request["status"] != "waiting":
            return f"Request {number} is already {request['status']}."
        request["status"] = "approved"
        self.menu_board.add_order(request["item"], request["customer"])
        return f"Request {number} approved."

    def reject(self, number):
        """Reject one waiting request. Nothing is ordered."""
        request = self.find(number)
        if request is None:
            return f"There is no request {number}."
        if request["status"] != "waiting":
            return f"Request {number} is already {request['status']}."
        request["status"] = "rejected"
        return f"Request {number} rejected."
