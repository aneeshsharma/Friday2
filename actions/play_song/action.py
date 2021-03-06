import requests
import json
import time
import subprocess as sp
import re
import os
import pafy
import vlc

with open('secret.json', 'r') as secret_file:
    data = secret_file.read()
    config = json.loads(data)
    key = config['apiKey']


def getId(keyword):
    url = "https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=2&order=viewCount&q={}&key={}".format(
        keyword, key)
    res = requests.get(url)
    video_id = res.json()['items'][0]['id']['videoId']
    return video_id


def playVideo(keyword, callback=None, endcallback=None):
    video_id = getId(keyword)

    url = 'http://youtube.com/watch?v=' + video_id
    video = pafy.new(url)
    best = video.getbest()
    playurl = best.url
    player = vlc.MediaPlayer(playurl)
    player.audio_set_volume(100)
    if callback:
        callback()
    player.play()
    time.sleep(5)
    while player.is_playing():
        time.sleep(1)
    endcallback()


def sendResult():
    result = {'text': 'playing...'}
    requests.post('http://localhost:5000/complete',
                  json={'id': id, 'result': result})


def endPlayback():
    time.sleep(1)
    os.system('pkill vlc')
    print('Playback ended')


if __name__ == "__main__":
    id = os.environ['TASK_ID']

    task_data = requests.get('http://localhost:5000/command?id='+id)
    command = task_data.json()['command']['command']
    print(command)
    search = re.sub('^play song$', '', command)
    print('Searching ' + search + '...')
    playVideo(search, sendResult, endPlayback)
