# Import libraries
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image
import streamlit as st

# Load API Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("API key not found. Please set it in the .env file.")
else:
    genai.configure(api_key=api_key)

# Function to load a model for diet planning
def get_response_diet(prompt, input):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')  # Replace with valid model later
        response = model.generate_content([prompt, input])
        return response.text
    except Exception as e:
        st.error(f"Error in diet planning: {e}")
        return "Could not generate diet response."

# Function to load a model for nutrition analysis
def get_response_nutrition(image, prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')  # Replace with valid model later
        response = model.generate_content([image[0], prompt])
        return response.text
    except Exception as e:
        st.error(f"Error in nutrition analysis: {e}")
        return "Could not generate nutrition response."

# Preprocess image data
def prep_image(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded!")

# Configuring Streamlit App
st.set_page_config(page_title="Health Management: Nutrition Calculator & Diet Planner", layout="wide")

# Custom styles
st.markdown(
    """
    <style>
    .title {
        font-size: 2.5em;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
    }
    .header {
        background-color: #f5f5f5;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True
)

# Display logo
st.markdown('<div class="title">Health: Nutrition Calculator & Diet Planner</div>', unsafe_allow_html=True)

section_choice1 = st.radio("Choose Section:", ("Nutrition Calculator", "Diet Planner"))

# If choice is nutrition calculator
if section_choice1 == "Nutrition Calculator":
    with st.container():
        st.markdown('<div class="header">Upload an Image</div>', unsafe_allow_html=True)
        upload_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        image = ""
        if upload_file is not None:
            image = Image.open(upload_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

        input_prompt_nutrition = """
        You are an expert Nutritionist. As a skilled nutritionist, you're required to analyze the food items
        in the image and determine the total nutrition value. 
        Additionally, you need to furnish a breakdown of each food item along with its respective content.

        Food item, Serving size, Total Cal., Protein (g), Fat,
        Carb (g), Fiber (g), Vit B-12, Vit B-6,
        Iron, Zinc, Mang.

        Use a table to show the above information.
        """
        if st.button("Calculate Nutrition Value!", key="nutrition_calc"):
            image_data = prep_image(upload_file)
            response = get_response_nutrition(image_data, input_prompt_nutrition)
            st.subheader("Nutrition AI: ")
            st.write(response)

# If choice is diet planner
if section_choice1 == "Diet Planner":
    with st.container():
        st.markdown('<div class="header">Plan Your Diet</div>', unsafe_allow_html=True)
        input_prompt_diet = """
        You are an expert Nutritionist. 
        If the input contains a list of items like fruits or vegetables, you have to give a diet plan and suggest
        breakfast, lunch, and dinner regarding the given item.
        If the input contains numbers, you have to suggest a diet plan for breakfast, lunch, and dinner within
        the given number of calories for the whole day.

        Return the response using markdown.
        """
        input_diet = st.text_area("Input the list of items that you have at home or how many calories you want to intake per day:")
        if st.button("Plan My Diet!", key="diet_plan"):
            response = get_response_diet(input_prompt_diet, input_diet)
            st.subheader("Diet AI: ")
            st.write(response)
