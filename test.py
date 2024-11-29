#from langchain_community.llms import HuggingFaceEndpoint
#from langchain.prompts import PromptTemplate
#from decouple import config
#HUGGINGFACEHUB_API_TOKEN = config('HUGGINGFACEHUB_API_TOKEN')

#template="<s>[INST]Write short answer of </s>{question}[/INST]"

#prompt_template = PromptTemplate.from_template(template)
#formatted_prompt_template = prompt_template.format(
    #question="i am sad,can you share some funny jokes,so that i can get rid of it?"
#)

#repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
#llm = HuggingFaceEndpoint(repo_id=repo_id,
#huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN)
#response = llm.invoke(formatted_prompt_template)
#print(response)


import streamlit as st
from langchain_community.llms import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from decouple import config
from PIL import Image
import requests
from bs4 import BeautifulSoup

# Load the Hugging Face API token
HUGGINGFACEHUB_API_TOKEN = config('HUGGINGFACEHUB_API_TOKEN')

# Initialize the Hugging Face model endpoint
repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
llm = HuggingFaceEndpoint(repo_id=repo_id, huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN)

# Define the prompt template
template = "<s>[INST]Answer based on the context: {context} and question: {question}[/INST]>"
prompt_template = PromptTemplate.from_template(template)

# Define a function to retrieve current information dynamically
def get_current_info(query):
    if "current prime minister of nepal" in query.lower():
        url = "https://en.wikipedia.org/wiki/Prime_Minister_of_Nepal"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract the name of the current prime minister (example structure)
        pm_info = soup.find("table", {"class": "infobox"}).find("tr", text="Prime Minister").find_next_sibling("tr").get_text()
        return f"The current Prime Minister of Nepal is {pm_info}."
    return None

# Custom CSS for styling the interface with animation
st.markdown("""
    <style>
    body {
        font-family: Arial, sans-serif;
    }
    .center-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        background-color: #f9f9f9;
    }
    .title {
        font-size: 32px;
        font-weight: bold;
        color: #2E8B57;
        margin-bottom: 20px;
    }
    .input-container {
        position: relative;
        width: 60%;
        max-width: 600px;
        margin-bottom: 20px;
    }
    .actions button {
        padding: 10px 20px;
        border: none;
        border-radius: 25px;
        background-color: #007BFF;
        color: white;
        font-size: 14px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .actions button:hover {
        background-color: #0056b3;
    }
    /* Animation for greeting message */
    .animated-message {
        font-size: 24px;
        font-weight: bold;
        color: black;
        text-align: center;
        animation: slideIn 2s ease-out;
    }

    /* Keyframes for animation */
    @keyframes slideIn {
        0% {
            opacity: 0;
            transform: translateX(-100%);
        }
        50% {
            opacity: 0.5;
            transform: translateX(0);
        }
        100% {
            opacity: 1;
            transform: translateX(0);
        }
    }
    </style>
""", unsafe_allow_html=True)

# App title
st.markdown("<h1 class='title'>SAARATHI</h1>", unsafe_allow_html=True)

# Display animated greeting message just above the search bar
st.markdown("<p class='animated-message'>Namaskar, how can I assist you?</p>", unsafe_allow_html=True)

# Sidebar navigation
page = st.sidebar.selectbox("Choose a Section", ["Ask a Question", "Analyze an Image"])

# Question handling page
if page == "Ask a Question":
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    user_input = st.text_input("🔍 Enter your question here:",placeholder="Ask Saarathi...")
    submit = st.button("Submit")  # Move Submit button here below the input
    st.markdown('</div>', unsafe_allow_html=True)

    if submit and user_input:  # Handle input only when Submit is clicked
        # Try fetching current info if the query demands it
        current_info = get_current_info(user_input)
        if current_info:
            st.write("Answer:")
            st.write(current_info)
        else:
            # Generate response from Hugging Face model
            formatted_prompt = prompt_template.format(question=user_input, context="general")
            try:
                response = llm.invoke(formatted_prompt)
                st.write("Answer:")
                st.write(response)
            except Exception as e:
                st.error("An error occurred while fetching the response.")
                st.error(f"Details: {e}")

# Image analysis page
elif page == "Analyze an Image":
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        st.success("Image uploaded successfully!")

        # Input for questions related to the image
        image_question = st.text_input("Ask a question about the image:", placeholder="What do you want to know about this image?")
        submit_image = st.button("Analyze Image")  # Add a Submit button for images
        if submit_image and image_question:
            # Mock context (replace with real model integration)
            image_context = "visual context of the uploaded image"
            formatted_prompt = prompt_template.format(context=image_context, question=image_question)
            try:
                response = llm.invoke(formatted_prompt)
                st.write("Answer:")
                st.write(response)
            except Exception as e:
                st.error("An error occurred while analyzing the image.")
                st.error(f"Details: {e}")

# Footer
st.sidebar.markdown("<p style='color: gray;'>© 2024 SAARATHI. All rights reserved.</p>", unsafe_allow_html=True)




