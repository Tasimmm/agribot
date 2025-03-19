import os
import streamlit as st
import google.generativeai as gen_ai
import speech_recognition as sr
from langdetect import detect
from openai import Image as Dalle

# Set your Google API Key
GOOGLE_API_KEY = "AIzaSyACdV7wgz84umfx8q4gwW-On57UVGo_6Ic"
# Set your OpenAI API Key for DALL-E
OPENAI_API_KEY = "your_openai_api_key_here"

# Configure APIs
gen_ai.configure(api_key=GOOGLE_API_KEY)
Dalle.api_key = OPENAI_API_KEY
model = gen_ai.GenerativeModel('gemini-pro')

st.set_page_config(
    page_title="Mini Project",
    page_icon=":brain:"  # Favicon emoji
)

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Display the chatbot's title on the page
st.title("AGRICULTURAL BOT")

# Sidebar for language selection
st.sidebar.header("Settings")
language_options = ["English", "Hindi", "Malayalam", "Kannada", "Tamil"]
language_map = {
    "English": "en",
    "Hindi": "hi",
    "Malayalam": "ml",
    "Kannada": "kn",
    "Tamil": "ta"
}
selected_language = st.sidebar.selectbox("Select your language:", language_options)

# Display the chat history
if st.session_state.chat_session.history:
    for message in st.session_state.chat_session.history:
        try:
            if isinstance(message, dict):
                role = translate_role_for_streamlit(message['role'])
                text = message['parts'][0]['text']
            else:
                role = translate_role_for_streamlit(message.role)
                text = message.parts[0].text

            with st.chat_message(role):
                st.markdown(text)

        except AttributeError:
            st.error("Error accessing message attributes.")

# System instruction for context
system_instruction = f"You are an expert chatbot that only responds to agriculture-related queries in {selected_language}."

# Input field for user's message
user_prompt = st.chat_input("Ask Gemini-Pro...")

if user_prompt:
    # Prepend system instruction to user prompt
    full_prompt = f"{system_instruction}\nUser: {user_prompt}\nAssistant:"

    # Add user's message to chat and display it
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Use st.spinner to indicate that processing is happening
    with st.spinner("Thinking..."):
        try:
            # Send the full prompt to Gemini-Pro and get the response
            gemini_response = st.session_state.chat_session.send_message(full_prompt)

            # Display Gemini-Pro's response
            response_text = gemini_response.text  # The response should be in the selected language.
            with st.chat_message("assistant"):
                st.markdown(response_text)

            # Update the chat session history
            st.session_state.chat_session.history.append({"role": "model", "parts": [{"text": response_text}]})

            # Generate and display an image related to the user's query
            with st.spinner("Generating related image..."):
                try:
                    image_prompt = f"Agriculture-related: {user_prompt}"
                    response = Dalle.create(prompt=image_prompt, n=1, size="512x512")
                    image_url = response['data'][0]['url']
                    st.image(image_url, caption="Related Image", use_column_width=True)
                except Exception as e:
                    st.warning("Unable to generate an image for the query.")

        except Exception as e:
            st.error(f"Error occurred: {str(e)}")

# Voice input feature
if st.button("Speak"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        st.write("Processing...")
        try:
            # Convert audio to text using Google Speech Recognition
            voice_input = recognizer.recognize_google(audio, language=language_map[selected_language])
            st.chat_message("user").markdown(voice_input)

            # Automatically detect the language of the voice input
            detected_language = detect(voice_input)

            # Check if the detected language is one of the supported languages
            if detected_language not in language_map.values():
                detected_language = 'en'  # Default to English if unsupported

            # Use detected or selected language for response contextually.
            full_voice_input = f"{system_instruction}\nUser: {voice_input}\nAssistant:"

            with st.spinner("Thinking..."):
                try:
                    gemini_response = st.session_state.chat_session.send_message(full_voice_input)

                    # Display Gemini-Pro's response in detected or selected language.
                    response_text = gemini_response.text  # The response should be in the selected or detected language.
                    with st.chat_message("assistant"):
                        st.markdown(response_text)

                    # Update chat session history
                    st.session_state.chat_session.history.append({"role": "model", "parts": [{"text": response_text}]})

                    # Generate and display an image related to the voice input
                    with st.spinner("Generating related image..."):
                        try:
                            image_prompt = f"Agriculture-related: {voice_input}"
                            response = Dalle.create(prompt=image_prompt, n=1, size="512x512")
                            image_url = response['data'][0]['url']
                            st.image(image_url, caption="Related Image", use_column_width=True)
                        except Exception as e:
                            st.warning("Unable to generate an image for the query.")

                except Exception as e:
                    st.error(f"Error occurred: {str(e)}")

        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio.")
        except sr.RequestError:
            st.error("Could not request results from Google Speech Recognition service.")
