import os
from pytube import YouTube
from django.shortcuts import render, redirect
from pytube.exceptions import RegexMatchError

def index(request):

    # Set a default value for url
    url = request.GET.get('url')

    # global message = ''
    
    if request.method == "GET":
        if url:
            try:
                # Create a YouTube object
                yt = YouTube(url)

                # Get the highest resolution video stream
                video = yt.streams.filter(progressive=True).get_highest_resolution()

                # Define Download location
                download_location = os.path.expanduser("~") + '/Downloads'

                # Download video
                video.download(download_location)

                # To reset the URL after a successful download, redirect the user to the same page after the download is complete
                return redirect('home')

            except(RegexMatchError, KeyError, AttributeError):

                return render(request, 'index.html') 
        else:

            return render(request, 'index.html')

    else:
        pass

    return render(request, 'index.html')