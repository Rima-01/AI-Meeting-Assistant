import openai
import os
import whisper
from openai import OpenAI
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
# Get OpenAI API Key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Debugging: Print API key (Remove after confirming)
print("OpenAI API Key in utils.py:", openai.api_key)

# Check if the API key is loaded correctly (Optional, for debugging)
if not openai.api_key:
    raise ValueError("⚠️ OpenAI API Key not found! Make sure it's set in the .env file.")
    
#openai.api_key = "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"
#client = openai.OpenAI(api_key=api_key)
client = OpenAI(api_key="OPENAI_API_KEY")

#def transcribe_audio(file_path):
#    with open(file_path, "rb") as audio_file:
#        transcript = openai.Audio.transcribe("whisper-1", audio_file)
#        return transcript["text"]
#    with open(file_path, "rb") as audio_file:
#        response = openai.audio.transcriptions.create(   
#            model="whisper-1",
#            file=audio_file
#        )
#    return response.text

#openai.api_key = "OPENAI_API_KEY"
def transcribe_audio(file_path):
    """
    Transcribes an audio file using local Whisper (No API key required).  
    """
    model = whisper.load_model("base")  #  
    result = model.transcribe(file_path)
    return result["text"]

def summarize_meeting(transcript):
    prompt = f"""
    Based on the following meeting transcript, create:
    1. A bullet-point summary of key discussion points.
    2. An action log with 'Date', 'Action', 'Owner', and 'Status'.
    
    Meeting Transcript:
    {transcript}
    
    Format:
    ## Summary:
    - Bullet Point 1
    - Bullet Point 2
    - Bullet Point 3

    ## Action Log:
    | Date | Action | Owner | Status |
    |------|--------|--------|--------|
    | YYYY-MM-DD | Action description | Assigned person | Pending/In Progress/Completed |
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]