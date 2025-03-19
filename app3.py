import os
import streamlit as st
import google.generativeai as gen_ai
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

# Set your Google API Key
GOOGLE_API_KEY = "AIzaSyC0AoNXSB5a24mPvyBgXXgruz5OLs9Ka1I"

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

st.set_page_config(
    page_title="agribot",
    page_icon=":leaf:"  # Favicon emoji
)

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Display the chatbot's title on the page
st.title("agribot")

# Language selection
language = st.selectbox("Choose your response language:", ["English", "Hindi", "Malayalam", "Kannada"])
language_map = {
    "English": "en",
    "Hindi": "hi",
    "Malayalam": "ml",
    "Kannada": "kn"
}

# Display the chat history
if st.session_state.chat_session.history:
    for message in st.session_state.chat_session.history:
        try:
            # Ensure message is a dictionary and has required keys
            if isinstance(message, dict):
                role = translate_role_for_streamlit(message.get('role', 'user'))
                parts = message.get('parts', [{}])

                if parts and isinstance(parts[0], dict):
                    text = parts[0].get('text', '')

                    # Render the chat message
                    with st.chat_message(role):
                        st.markdown(text)
        except Exception as e:
            st.error(f"Error displaying message: {str(e)}")

# System instruction for context
system_instruction = "You are an expert chatbot that only responds to agriculture-related queries."

# Input field for user's message
user_prompt = st.chat_input("Ask Gemini-Pro...")

# Process user prompt immediately after it's entered
if user_prompt:
    full_prompt = f"{system_instruction}\nUser: {user_prompt}\nAssistant:"
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.spinner("Thinking..."):
        try:
            gemini_response = st.session_state.chat_session.send_message(full_prompt)
            response_text = gemini_response.text

            # Check if the response is agriculture-related
            if "agriculture" in user_prompt.lower() or "farm" in user_prompt.lower() or "crop" in user_prompt.lower():
                # Display response
                with st.chat_message("assistant"):
                    st.markdown(response_text)

                # Generate audio response in selected language
                lang_code = language_map[language]
                temp_dir = "C:/Temp"
                os.makedirs(temp_dir, exist_ok=True)

                audio_file = os.path.join(temp_dir, "response.mp3")
                tts = gTTS(text=response_text, lang=lang_code)
                tts.save(audio_file)

                if os.path.exists(audio_file):
                    audio = AudioSegment.from_mp3(audio_file)
                    play(audio)

            else:
                # Notify the user that their query is out of scope
                out_of_scope_message = "I'm here to assist you with agriculture-related topics only. Please ask a relevant question."
                with st.chat_message("assistant"):
                    st.markdown(out_of_scope_message)

            # Update chat session history
            st.session_state.chat_session.history.append({"role": "model", "parts": [{"text": response_text}]})

        except Exception as e:
            st.error(f"Error occurred: {str(e)}")

# Voice input feature
voice_language = st.selectbox("Choose your voice input language:", ["English", "Hindi", "Malayalam", "Kannada"])

if st.button("Speak"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        st.write("Processing...")
        try:
            # Use the selected language for speech recognition
            voice_lang_code = language_map[voice_language]
            voice_input = recognizer.recognize_google(audio, language=voice_lang_code)
            st.chat_message("user").markdown(voice_input)

            full_voice_input = f"{system_instruction}\nUser: {voice_input}\nAssistant:"

            with st.spinner("Thinking..."):
                try:
                    gemini_response = st.session_state.chat_session.send_message(full_voice_input)
                    response_text = gemini_response.text

                    if "agriculture" in voice_input.lower() or "farm" in voice_input.lower() or "crop" in voice_input.lower():
                        with st.chat_message("assistant"):
                            st.markdown(response_text)

                        # Generate audio response in selected language
                        lang_code = language_map[voice_language]
                        temp_dir = "C:/Temp"  # Define temp_dir in the voice section too
                        os.makedirs(temp_dir, exist_ok=True)

                        audio_file = os.path.join(temp_dir, "response.mp3")
                        tts = gTTS(text=response_text, lang=lang_code)
                        tts.save(audio_file)

                        if os.path.exists(audio_file):
                            audio = AudioSegment.from_mp3(audio_file)
                            play(audio)

                    else:
                        out_of_scope_message = "I'm here to assist you with agriculture-related topics only. Please ask a relevant question."
                        with st.chat_message("assistant"):
                            st.markdown(out_of_scope_message)

                    # Update chat session history
                    st.session_state.chat_session.history.append({"role": "model", "parts": [{"text": response_text}]})

                except Exception as e:
                    st.error(f"Error occurred: {str(e)}")

        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio.")
        except sr.RequestError:
            st.error("Could not request results from Google Speech Recognition service.")
