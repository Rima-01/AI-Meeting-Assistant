from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
import markdown
import os
from .models import Meeting
from .utils import transcribe_audio, summarize_meeting

# Define the path to store uploaded audio files
AUDIO_FILE_PATH = "/home/ec2-user/environment/ai_meeting_wizard_backend/temp/"

@api_view(["POST"])
def process_meeting(request):
    """
    Handles the audio file upload, transcribes it, generates a bullet-point summary,
    creates an action log, and stores the data in the database.
    """
    if "audio" not in request.FILES:
        return Response({"error": "No audio file provided"}, status=400)

    audio_file = request.FILES["audio"]
    
    # Ensure temp directory exists
    os.makedirs(AUDIO_FILE_PATH, exist_ok=True)

    # Save the uploaded audio file to the temp directory
    file_path = os.path.join(AUDIO_FILE_PATH, audio_file.name)
    with open(file_path, "wb+") as f:
        for chunk in audio_file.chunks():
            f.write(chunk)

    # Transcribe the audio file
    transcript = transcribe_audio(file_path)

    # Generate summary and action log using GPT-4
    summary_action_log = summarize_meeting(transcript)

    # Split the AI-generated response into summary and action log
    if "## Action Log:" in summary_action_log:
        summary, action_log = summary_action_log.split("## Action Log:")
    else:
        summary, action_log = summary_action_log, "No action log generated."

    # Save to PostgreSQL database
    meeting = Meeting.objects.create(
        title="Meeting Title",
        transcript=transcript.strip(),
        summary=summary.strip(),
        action_log=action_log.strip()
    )

    return Response({
        "message": "Meeting processed successfully",
        "meeting_id": meeting.id,
        "summary": summary.strip(),
        "action_log": action_log.strip()
    })


@api_view(["POST"])
def add_meeting(request):
    """
    API to manually add a new meeting with a transcript, summary, and action log.
    """
    data = request.data
    title = data.get("title")
    transcript = data.get("transcript")
    summary = data.get("summary")
    action_log = data.get("action_log")

    # Validate required fields
    if not title or not transcript:
        return Response({"error": "Title and transcript are required."}, status=400)

    # Create a new meeting record
    meeting = Meeting.objects.create(
        title=title,
        transcript=transcript.strip(),
        summary=summary.strip() if summary else "No summary provided.",
        action_log=action_log.strip() if action_log else "No action log provided."
    )

    return Response({"message": "Meeting added successfully", "meeting_id": meeting.id})


@api_view(["GET"])
def get_meeting_details(request, meeting_id):
    """
    Retrieves meeting details including transcript, summary, and action log.
    Converts Markdown to HTML for better frontend display.
    """
    meeting = get_object_or_404(Meeting, id=meeting_id)

    return Response({
        "title": meeting.title,
        "transcript": meeting.transcript,
        "summary": markdown.markdown(meeting.summary),  # Convert Markdown to HTML
        "action_log": markdown.markdown(meeting.action_log)  # Convert table format to HTML
    })


@api_view(["GET"])
def list_meetings(request):
    """
    Returns a list of all stored meetings with summaries.
    """
    meetings = Meeting.objects.all().order_by("-created_at")  # Order by most recent
    data = [{"id": m.id, "title": m.title, "summary": m.summary[:100] + "..."} for m in meetings]

    return Response({"meetings": data})
