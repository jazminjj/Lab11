# README.md
# Author: Jazmin Joseph

My assistant, Mocha, answers customers questions about menu prices for a coffee shop. A MenuBoard tool looks up prices, and the MenuHelper class keeps the conversation and its hisory. Everything is mock: therelies come from keyword rules in if statements, with no AI model, API, or internet. Any question about allergies, gluten, dairy, or ingredients goes to a staff memeber because a wrong answer could possible make someone sick. If this used real customer data, it could leak private information or quote an incorrect price from an old menu.

# week 11
I added a local model to Mocha so that it can answer questions that my rules don't cover. When I asked "what time do you open?" the model answered the cafe opens 7am, which is exactly the time i put in the instructions. When I asked "is the latte vegan" the bot made up an answer about the ingredients, even though my instructions do not ocver that. I kept the menu prices and the allergry handoff words in the code because an incorrect answer about allergy or price could negatively affect a customer and my business. I learned that the model only knows what i put in the instructions and that its good for casual questions but not specific facts or questions.

# Week 12 Lab
Mocha's model now chooses when to use a tool instead of keyword rules. When I asked the model how much is a latte, it handled it well and told me the price is $4.50. In my instructions i told the model to never guess a name and to always ask so it did not refuse that request when I asked to place a pickup order without stating a name. The line under Instructions in my_main.py file states, "TO request a pickup order you need the item and the customers name. Never guess a name." If i hadn't added that line to my instructions, it wouldve made up a name. I then gave the model my name and my order was sent to the staff for pickup, which they then have to approve. 
    Here is our conversation: 
You: hello
Mocha: hello! how can i help you today?
You: how much is a latte?
Mocha: a latte is $4.50.
You: please order a latte for pickup
Mocha: could you please provide the customer's name for the pickup order?
You: my name is Dana Cruz
Mocha: your latte order for Dana Cruz has been sent to staff for pickup.
You: is the croissant gluten free?
Mocha: I can't help with that allergy or ingredient question. I'm passing you to a human agent.
You: quit
Messages in this conversation: 12
Staff review
Request 1: Dana Cruz, latte
Approve? yes or noyes
Request 1 approved.
Orders: 1