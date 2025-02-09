#from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
import markdown
from .models import Meeting
from .utils import transcribe_audio, summarize_meeting

@api_view(["POST"])
def process_meeting(request):
    """
    Handles the audio file upload, transcribes it, generates a bullet-point summary,
    creates an action log, and stores the data in the database.
    """
    if "audio" not in request.FILES:
        return Response({"error": "No audio file provided"}, status=400)

    audio_file = request.FILES["audio"]
    
    # Save audio file locally (optional, for debugging)
    file_path = f"temp/{audio_file.name}"
    with open(file_path, "wb+") as f:
        for chunk in audio_file.chunks():
            f.write(chunk)

    # Transcribe the audio file
    transcript = transcribe_audio(file_path)

    # Generate summary and action log
    summary_action_log = summarize_meeting(transcript)

    # Split the AI-generated response into summary and action log
    if "## Action Log:" in summary_action_log:
        summary, action_log = summary_action_log.split("## Action Log:")
    else:
        summary, action_log = summary_action_log, "No action log generated."

    # Save the meeting details to the database
    meeting = Meeting.objects.create(
        title="Meeting Title",  # You may modify this to allow dynamic titles
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


@api_view(["GET"])
def get_meeting_details(request, meeting_id):
    """
    Retrieves meeting details including transcript, summary, and action log.
    Converts Markdown to HTML for better formatting in frontend.
    """
    meeting = get_object_or_404(Meeting, id=meeting_id)

    return Response({
        "title": meeting.title,
        "transcript": meeting.transcript,
        "summary": markdown.markdown(meeting.summary),  # Converts Markdown to HTML
        "action_log": markdown.markdown(meeting.action_log)  # Converts table format to HTML
    })


@api_view(["GET"])
def list_meetings(request):
    """
    Returns a list of all stored meetings with summaries.
    """
    meetings = Meeting.objects.all().order_by("-created_at")  # Order by most recent
    data = [{"id": m.id, "title": m.title, "summary": m.summary[:100] + "..."} for m in meetings]

    return Response({"meetings": data})
