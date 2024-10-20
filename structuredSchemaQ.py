import streamlit as st
import os
import google.generativeai as genai
import typing_extensions as typing
import enum
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")

# Configure API key
genai.configure(api_key=api_key)

# Define Enums and TypedDicts for the schema
class Grade(enum.Enum):
    A_PLUS = "a+"
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    F = "f"

class Recipe(typing.TypedDict):
    recipe_name: str
    ingredients: list[str]
    grade: Grade

# Streamlit interface
st.title("Gemini API - Structured Schema-Based Responses")
st.write("Enter a prompt, and the Gemini API will return a structured JSON response based on a predefined schema.")

# User input
user_input = st.text_input("Enter your prompt (e.g., 'List about 10 cookie recipes, grade them based on popularity'):")

# Schema selection: Recipes (you can add more types here if needed)
schema_choice = st.selectbox("Choose the schema type:", ["Recipe List"])

# Generate content based on schema
if user_input and st.button("Generate Response"):
    # Define generation configuration with schema
    if schema_choice == "Recipe List":
        generation_config = genai.GenerationConfig(
            response_mime_type="application/json",
            response_schema=list[Recipe]
        )

        # Generate content using the Gemini API
        result = genai.GenerativeModel("gemini-1.5-pro-latest").generate_content(
            user_input,
            generation_config=generation_config
        )

        # Display the result as formatted JSON
        st.success("Generated JSON Response:")
        st.json(result.text)

# Additional info about schema and structured output
st.sidebar.title("Schema and Structured Output")
st.sidebar.write("This example demonstrates how to generate structured JSON responses based on a schema defined using Python typing annotations.")
st.sidebar.write("For this demo, the schema represents a list of recipes, each with a recipe name, ingredients, and a grade representing the popularity of the recipe.")
