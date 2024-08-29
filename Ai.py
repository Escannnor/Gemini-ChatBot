import customtkinter as ctk
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os

API_KEY = os.getenv('GEMINI_API_KEY')

if not API_KEY:
    raise ValueError("API key not found. Please set the GEMINI_API_KEY environment variable.")

class GeminiAI:
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }
        
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

    def generate_content(self, prompt, custom_safety_settings=None, custom_generation_config=None):
        try:
            safety_settings = custom_safety_settings or self.safety_settings
            generation_config = custom_generation_config or self.generation_config

            response = self.model.generate_content(
                prompt,
                safety_settings=safety_settings,
                generation_config=generation_config
            )

            print("Response attributes:", dir(response))

            return {
                "text": response.text,
                # Uncomment the next line if safety_ratings is indeed part of the response
                # "safety_ratings": response.safety_ratings
            }

        except Exception as e:
            return {"error": str(e)}

    def set_safety_settings(self, new_settings):
        self.safety_settings.update(new_settings)

    def set_generation_config(self, new_config):
        self.generation_config.update(new_config)

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("GeminiAI Content Generator")
        self.geometry("600x400")

        self.api_key = API_KEY
        self.gemini = GeminiAI(self.api_key)

        self.create_widgets()

    def create_widgets(self):
        self.prompt_label = ctk.CTkLabel(self, text="Enter your prompt:")
        self.prompt_label.pack(pady=10)

        self.prompt_entry = ctk.CTkEntry(self, width=500)
        self.prompt_entry.pack(pady=10)

        self.generate_button = ctk.CTkButton(self, text="Generate", command=self.generate_content)
        self.generate_button.pack(pady=10)

        self.output_text = ctk.CTkTextbox(self, width=500, height=200)
        self.output_text.pack(pady=10)

    def generate_content(self):
        prompt = self.prompt_entry.get()
        if prompt:
            result = self.gemini.generate_content(prompt)
            if "error" in result:
                self.output_text.delete("1.0", ctk.END)
                self.output_text.insert(ctk.END, f"An error occurred: {result['error']}")
            else:
                self.output_text.delete("1.0", ctk.END)
                self.output_text.insert(ctk.END, result["text"])
        else:
            self.output_text.delete("1.0", ctk.END)
            self.output_text.insert(ctk.END, "Please enter a prompt.")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
