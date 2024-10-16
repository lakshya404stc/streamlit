import streamlit as st
from google.cloud import speech
import os
from utilities.index import Utilities
from dotenv import load_dotenv
from google.oauth2 import service_account

# Load environment variables from .env file
load_dotenv()

# Reconstruct the credentials dictionary
google_credentials = {
    "type": os.getenv("GOOGLE_TYPE"),
    "project_id": os.getenv("GOOGLE_PROJECT_ID"),
    "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("GOOGLE_PRIVATE_KEY").replace('\\n', '\n'),  # Replacing escaped newlines
    "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
    "client_id": os.getenv("GOOGLE_CLIENT_ID"),
    "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
    "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("GOOGLE_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("GOOGLE_CLIENT_X509_CERT_URL")
}

# Use the credentials to authenticate the SpeechClient
credentials = service_account.Credentials.from_service_account_info(google_credentials)

# Initialize the SpeechClient with these credentials
client = speech.SpeechClient(credentials=credentials)

def main():
    st.title("CuriousPm assignment")
    st.subheader("This assignment is submitted by Lakshya Gupta")

    video_file = st.file_uploader("Upload a video file", type=["mp4"])
    
    if video_file:
        video_path = "temp_video.mp4"
        with open(video_path, "wb") as f:
            f.write(video_file.read())
        
        st.write("Video uploaded successfully. Generating transcription")

        transcription_map = Utilities.create_audio_transcription_map(video_path)

        st.write("Generated Original 1-Second Transcription Map")
        corrected_transcription_map = Utilities.correct_transcription_map(transcription_map)

        st.write("Generated Correct 1-Second Transcription Map")

        st.write("Generating audio files for each time range...")
        Utilities.generate_audio_files_from_map(corrected_transcription_map)

        st.write("Audio generation complete! Joining the audio files into one...")

        final_audio_path = "final_output.wav"
        Utilities.join_audio_files_from_map(corrected_transcription_map, output_file=final_audio_path)

        st.write("All audio files joined successfully! Attaching the audio to the video...")

        original_video_name = video_file.name.split('.')[0]
        output_video_path = f"out_{original_video_name}.mp4"

        Utilities.attach_audio_to_video(video_path, final_audio_path, output_video_path)

        st.video(output_video_path)

        os.remove(video_path)
        os.remove(final_audio_path)


if __name__ == "__main__":
    main()

