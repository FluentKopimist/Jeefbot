import requests, bs4, os, json
vredditLink = "https://old.reddit.com/r/nextfuckinglevel/comments/kn8qs4/dont_touch_the_trash_can/"

url = vredditLink + '.json'
print (url)

## append .json to the end of the url, search json for fallback url, video is under ex. dash_720 the audio would be under the same link, but dash_audio, use ffmpeg to put audio and video together and make a single webm
## learn to make discord bot, post webm, delete webm, ignore posts that contain !fuckoff
