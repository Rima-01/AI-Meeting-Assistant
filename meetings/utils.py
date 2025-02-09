import openai

openai.api_key = "YOUR_OPENAI_API_KEY"

def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript["text"]
        
import openai

openai.api_key = "YOUR_OPENAI_API_KEY"

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