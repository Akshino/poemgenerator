import os
import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64

# Configure the Gemini API
genai.configure(api_key="AIzaSyClqSzrXiCLgKeRJKGT2vYHAMi6lHbfVVw")

# Set up the generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1000,
    "response_mime_type": "text/plain",
}

# Initialize the GenerativeModel
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Function to generate audio using gTTS
def generate_audio(poem_text):
    try:
        # Generate audio file with gTTS
        tts = gTTS(text=poem_text, lang='en')
        tts.save("generated_poem.mp3")

        # Encode audio to base64
        with open("generated_poem.mp3", "rb") as f:
            audio_bytes = f.read()
        return base64.b64encode(audio_bytes).decode(), True
    except Exception as e:
        st.error(f"Error generating audio: {e}")
        return None, False

# Create the Streamlit app
st.title("Gemini AI Poem Generator")

# Input from user
theme = st.text_input("Enter a theme for the poem:", placeholder="e.g., Love, Nature, Friendship")

# Button to generate poem
if st.button("Generate Poem"):
    if theme:
        with st.spinner("Generating poem..."):
            # Start chat session
            chat_session = model.start_chat(
                history=[
                    {
                        "role": "user",
                        "parts": [f"Generate a poem on the theme: {theme}"],
                    },
                ]
            )

            # Send message to model and get response
            response = chat_session.send_message(f"Generate a poem on the theme: {theme}")

            # Display the generated poem
            st.write("### Generated Poem:")
            st.write(response.text)

            # Convert the poem to audio using gTTS
            with st.spinner("Converting poem to audio..."):
                audio_base64, success = generate_audio(response.text)

                if success:
                    # Display audio player
                    st.audio(f"data:audio/mp3;base64,{audio_base64}", format="audio/mp3")
                else:
                    st.error("Failed to generate audio.")
    else:
        st.warning("Please enter a theme before generating the poem.")
