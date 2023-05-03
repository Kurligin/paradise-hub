import youtube_dl
import vlc


VIDEO_URL = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

ydl = youtube_dl.YoutubeDL()

video = ydl.extract_info(
    VIDEO_URL,
    download=False,
)

url = video['url']

instance = vlc.Instance('--no-video')
player = instance.media_player_new()
media = instance.media_new(url)
player.set_media(media)

player.play()

while True:
    pass
