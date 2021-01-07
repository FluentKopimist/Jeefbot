import requests
import os
import json
import ffmpeg

#reddit_url = "https://old.reddit.com/r/aww/comments/kr98n2/the_corgi_express/"#vreddit video url with no audio
reddit_url = "https://old.reddit.com/r/leagueoflegends/comments/88rypt/jesus_christ_if_this_gets_enough_upvotes_it_will/" #example reddit url
#reddit_url = "https://old.reddit.com/r/nextfuckinglevel/comments/kn8qs4/dont_touch_the_trash_can/" #regular vreddit video with audio
json_url = reddit_url + ".json"
r = requests.get(json_url, headers={'User-agent': 'JeefBot'}) #connect to reddit using fake user agent so it doesn't kick us out for avoiding their api
r_dict = json.loads(r.text) #creates dictionary file with our json so we may query it for the values we need

#def create working directory
current_directory = os.getcwd()
final_directory = os.path.join(current_directory, r'Temp')
if not os.path.exists(final_directory):
   os.makedirs(final_directory)

try:
    video_url = r_dict[0]['data']['children'][0]['data']['secure_media']['reddit_video']['fallback_url'] #filter .json for video url
    print ("Found video url at: ", video_url)
    audio_url = r_dict[0]['data']['children'][0]['data']['url'] + "/DASH_audio.mp4" #the audio is stored at the same location and by appending /DASH_audio we can find it
    print ("Found audio url at: ", audio_url)
except:
    print ("As far as I can tell the url at:")
    print (reddit_url) 
    print ("Does not contain any video source.")
    print ("Please try another url.")
    from time import sleep
    sleep(5)

## todo Use requests to download files, use ffmpeg to put the audio and video together. learn how to use this in a discord bot setting.