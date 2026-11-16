# my_assistant.py
# Author: Jazmin Joseph

HANDOFF_WORDS = ["allerg", "gluten", "dairy", "ingredient"]
MAX_TOOL_ROUNDS = 3


class MenuHelper:
    def __init__(self, name, instructions, tools, model):
        """Set up one helper with its own name, instructions, tool, and history."""
        self.name = name
        self.instructions = instructions
        self.tools = tools
        self.model = model
        self.history = []

    def respond(self, user_message):
        """Record the user's message, choose a reply, record it, and return it."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        """Pass allergy question to a human. Send everything else to the model."""
        text = user_message.lower()
        if self.needs_human(text):
            return "I can't help with that allergy or ingredient question. I'm passing you to a human agent."
        return self.model_reply()

    def needs_human(self, text):
        """Return true if the message is about something a person must handle."""
        for word in HANDOFF_WORDS:
            if word in text:
                return True
        return False

    def model_reply(self):
        """Ask the model. Run each tool it asks for, then ask again, up to a limit."""
        rounds = 0
        while rounds < MAX_TOOL_ROUNDS:
            tool_list = self.tools.tool_list()
            decision = self.model.decide(self.instructions, self.history, tool_list)
            if decision is None:
                return "Sorry, I can't answer that right now. Please try again in a moment."
            if "text" in decision:
                return decision["text"]
            name = decision["tool"]
            arguments = decision["arguments"]
            result = self.tools.run(name, arguments, self.history)
            self.history.append(
                {
                    "role": "tool",
                    "tool_name": name,
                    "arguments": arguments,
                    "content": result,
                }
            )
            rounds += 1
        return "Sorry, I couldn't finish that. I'm passing you to a human agent."
