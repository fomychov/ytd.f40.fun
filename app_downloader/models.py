from django.db import models
import youtube_dl
from moviepy.editor import *
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django import forms

# Define a Django model to store information about the downloaded files
class Download(models.Model):
    url = models.CharField(max_length=200)
    format = models.CharField(max_length=10)
    quality = models.CharField(max_length=10)
    file = models.FileField(upload_to='downloads')

# Define a Django form to allow the user to input the YouTube URL and format
class DownloadForm(forms.Form):
    url = forms.CharField(label='YouTube URL')
    format = forms.ChoiceField(choices=[('audio', 'Audio'), ('video', 'Video')], label='Format')

# Define a Django view to handle the form submission and file download
def download(request, id):
    download = get_object_or_404(Download, id=id)
    
    # Serve the file to the user as a downloadable attachment
    response = FileResponse(download.file, as_attachment=True)
    return response

def download_form(request):
    if request.method == 'POST':
        form = DownloadForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            format = form.cleaned_data['format']
            
            ydl_opts = {
                'format': 'bestaudio/best' if format == 'audio' else 'bestvideo[height<=1080]/best[height<=1080]',
                'outtmpl': 'downloads/%(id)s.%(ext)s',
            }
            
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                file_url = info_dict['url']
                file_id = info_dict['id']
                file_ext = info_dict['ext']
                
                if format == 'video':
                    # Process the video to extract the audio
                    video = VideoFileClip(file_url)
                   
