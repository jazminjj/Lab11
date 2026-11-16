# Week 12 Answers

## Exercise 1
1. The messages the customer typed: I want to change my shipping address, It's order A102, 9 Pine Street, Tampa.
2. How many tool requests were refused, and why: Two requests were refused, order A100 and 123 Main St, Anytown, AN 12345. The customer did not type either of these.
3. If the customer now types "thanks", how many messages does Ollama receive on the next call? 14
4. Why does "Do you sell gift cards?" still go to a person, and why is that acceptable? It goes ot a person beacause Ollama doesnt have enough information to answer it correctly. So instead of making up an answer, it send the customer to staff member. This is acceptable because it ensures that the customer is recieving accurate information.

# Exercise 3
You: I want to change my shipping address
Sunny: Your request to change the shipping address has been submitted to staff for approval. They will review it and notify you once the change is processed.
You: quit
Messages in this conversation: 3
Staff review
Request 1: A100 to 123 Main St, Anytown, AN 12345
Approve? yes or no: no
Request 1 rejected.
A100 14 Bay Road
A101 3 Gull Lane
A102 88 Pier Street