import os
from dotenv import load_dotenv
from google import genai


# Load variables from .env file
load_dotenv()


class GeminiService:
    """
    Handles communication with Google's Gemini API.
    """

    def __init__(self):

        # Get Gemini API key from .env
        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. "
                "Please check your .env file."
            )

        # Create Gemini client
        self.client = genai.Client(
            api_key=self.api_key
        )

        # Gemini model
        self.model = "gemini-2.5-flash"


    def generate_response(self, prompt):
        """
        Sends a prompt to Gemini
        and returns the generated response.
        """

        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            return response.text

        except Exception as e:

            return f"Gemini API Error: {str(e)}"