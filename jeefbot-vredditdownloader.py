import requests
import os
import json

#json_url = "https://old.reddit.com/r/aww/comments/kr98n2/the_corgi_express/" + ".json" #vreddit video url with no audio
json_url = "https://old.reddit.com/r/leagueoflegends/comments/88rypt/jesus_christ_if_this_gets_enough_upvotes_it_will/" + ".json" #example reddit url
#json_url = "https://old.reddit.com/r/nextfuckinglevel/comments/kn8qs4/dont_touch_the_trash_can/" + ".json" #regular vreddit video with audio
r = requests.get(json_url, headers={'User-agent': 'JeefBot'}) #connect to reddit using fake user agent so it doesn't kick us out for avoiding their api
r_dict = json.loads(r.text) #creates dictionary file with our json so we may query it for the values we need

try:
    video_url = r_dict[0]['data']['children'][0]['data']['secure_media']['reddit_video']['fallback_url'] #filter .json for video url
    print ("Found video url at: ", video_url)
    audio_url = r_dict[0]['data']['children'][0]['data']['url'] + "/DASH_audio.mp4" #the audio is stored at the same location and by appending /DASH_audio we can find it
    print ("Found audio url at: ", audio_url)
except:
    print ("As far as I can tell, this link isn't a video.")




## append .json to the end of the url, search json for fallback url, video is under ex. dash_720 the audio would be under the same link, but dash_audio, use ffmpeg to put audio and video together and make a single webm
## learn to make discord bot, post webm, delete webm, ignore posts that contain !fuckof