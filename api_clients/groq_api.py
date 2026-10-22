import os
# os lets Python read environment variables such as GROQ_API_KEY.

from groq import Groq
# Groq is the Python library we installed.
# It lets our framework communicate with the Groq API.


class Groq_API:
    # This class will contain our Groq API methods.

    def __init__(self):
        # __init__ runs automatically when we create Groq_API().

        api_key = os.getenv("GROQ_API_KEY")
        # Read the Groq API key from the environment.
        # We do NOT hardcode the key in our Python code.

        self.client = Groq(api_key=api_key)
        # Create the Groq client using our API key.
        # self.client stores this client so other methods in this class
        # can use it.

    def ask_question(self, question):
        # question = the question we want to send to the AI.

        response = self.client.chat.completions.create(
            # Send a chat request to the Groq API.

            model="openai/gpt-oss-120b",
            # Tell Groq which AI model should generate the answer.

            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ]
            # Send our question as a user message.
        )

        return response
        # Return the AI response back to the test.