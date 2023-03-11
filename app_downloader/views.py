import os
import moviepy.editor as mp
from pytube import YouTube
from django.shortcuts import render, redirect
from pytube.exceptions import RegexMatchError


def index(request):

    url = request.GET.get('url')
    
    # Define Download location
    download_location = os.path.join(os.path.expanduser("~"), 'Downloads')

    if request.method == "GET":
        if url:
            if 'video' in request.GET:
                success = download_video(url, download_location)
                if success:
                    # To reset the URL after a successful download, redirect the user to the same page after the download is complete
                    return redirect('home')

            elif 'audio' in request.GET:
                success = download_audio(url, download_location)
                if success:
                    # To reset the URL after a successful download, redirect the user to the same page after the download is complete
                    return redirect('home')

            else:
                pass

    return render(request, 'index.html')


def download_video(url, download_location):
    try:
        # Create a YouTube object
        yt = YouTube(url)

        # Get the highest resolution video stream
        video = yt.streams.filter(progressive=True).get_highest_resolution()

        # Download video
        video.download(download_location)

        return True

    except (RegexMatchError, KeyError, AttributeError):
        return False


def download_audio(url, download_location):

    try:
        # Create a YouTube object
        yt = YouTube(url)

        # Get the highest quality audio stream
        print("Get the highest quality audio stream")
        audio_stream = yt.streams.filter(
            only_audio=True).order_by('abr').desc().first()

        # Download audio
        print('Download audio')
        audio_stream.download()
            
        # CONVERT THE DOWNLOADED AUDIO TO MP3 FORMAT
        # Load the audio file
        print('Load the audio file')
        audio_clip = mp.AudioFileClip(audio_stream.default_filename)

        # Set the output file name and extension
        print('Set the output file name and extension')
        output_file_name = audio_stream.default_filename.split(".")[0] + ".mp3"

        # Set the full path
        print('Set the full path')
        output_file_path = os.path.join(download_location, output_file_name)

        # Save the audio in mp3 format
        print('Save the audio in mp3 format')
        audio_clip.write_audiofile(output_file_path)

        # Delete the original audio file
        print('Delete the original audio file')
        os.remove(audio_stream.default_filename)

        return True

    except (RegexMatchError, KeyError, AttributeError):
        return False