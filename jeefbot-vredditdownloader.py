import requests
import os
import json
import subprocess
import ffmpeg

#This is a vredditdownloader function I am writing, to be implemented into a discord bot called "JeefBot" sometime in the future.

def main():
    
    video_identifier = 0; #video_identifier will be a global variable that will increment by 1 every time this is ran, identifying the videos and the audio that goes with it
    
    #uncomment whichever reddit url needed for debug
    #reddit_url = "https://old.reddit.com/r/aww/comments/kr98n2/the_corgi_express/"#example vreddit webm with no audio
    #reddit_url = "https://old.reddit.com/r/leagueoflegends/comments/88rypt/jesus_christ_if_this_gets_enough_upvotes_it_will/" #example reddit url containing no audio or video
    reddit_url = "https://old.reddit.com/r/nextfuckinglevel/comments/kn8qs4/dont_touch_the_trash_can/" #example vreddit webm with audio
    vreddit_dict{
  "working_directory": "",
  "audio_url": "",
  "video_url": 1964,
  "year": 2020
  }
    vreddit_dict = check_working_directory()
    find_vreddit_urls(reddit_url)
    download_vreddit_video(video_url, audio_url, temp_dir, video_identifier) #==================================== Apparently you cant return multiple values. look into dictionaries maybe?

def check_working_directory():

    #current_dir = os.getcwd() #gets program's current directory if you would like to use it that way, currently messed up because of the space in my username
    #current_dir = f'"{current_dir}"' #this was an attempt to fix by putting quotes around "current_dir" this didnt work either
    current_dir = "c:\jeefbot" #creates working directory in the c: drive where no spaces can get in my way
    temp_dir = os.path.join(current_dir, r'vredditdownloader')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    vreddit_dict['working_directory'] = temp_dir;
    return vreddit_dict;

def find_vreddit_urls(reddit_url):

    json_url = reddit_url + ".json"
    r = requests.get(json_url, headers={'User-agent': 'JeefBot'}) #connect to reddit using fake user agent so it doesn't kick us out for avoiding their api
    r_dict = json.loads(r.text) #creates dictionary file with our json so we may query it for the values we need

    try:
        video_url = r_dict[0]['data']['children'][0]['data']['secure_media']['reddit_video']['fallback_url'] #filter .json for video url
        print ("Found video url at: ", video_url)
        audio_url = r_dict[0]['data']['children'][0]['data']['url'] + "/DASH_audio.mp4" #the audio is stored at the same location and by appending /DASH_audio we can find it
        print ("Found audio url at: ", audio_url)
        
    except:
        print ("As far as I can tell the url at:")
        print (reddit_url) 
        print ("Does not contain any video source.") #-------------------------------------------log it instead of print
        
    return video_url;

def download_vreddit_video(video_url, audio_url, temp_dir, video_identifier):    
    try:
        print (video_url, audio_url, temp_dir, video_identifier) #just trying to see if i made it this far
        r = requests.get(video_url, stream = True) #requesting video from reddit
        with open(os.path.join(temp_dir ,'video' + video_identifier + '.mp4'), "wb") as f:
            for chunk in r.iter_content(chunk_size = 16*1024): #request file in chunks for speed and less ram usage
                f.write(chunk)
    except:
        print ("Something went wrong with the video request. probably bad url.")
    
    try:
        r = requests.get(audio_url, stream = True) #requesting audio from reddit
        with open(os.path.join(temp_dir ,'audio' + video_identifier + '.mp4'), "wb") as f:
            for chunk in r.iter_content(chunk_size = 16*1024): #request file in chunks for speed and less ram usage
                f.write(chunk)
    except:
        print ("No audio found, this video probably doesnt contain any audio source.")
    
    return;

def combine_with_ffmpeg(video_identifier, temp_dir):

     # combining audio and video into one file
    print("combining audio and video into one file")
    uncompressed_path = os.path.join(temp_dir, 'uncompressed' + video_identifier + '.mp4')
    subprocess.call(f"ffmpeg.exe -i {os.path.join(temp_dir ,'video' + video_identifier + '.mp4')} -i {os.path.join(temp_dir ,'audio' + video_identifier + '.mp4')} -c copy {uncompressed_path}", shell=True)

    return;

def compress_with_ffmpeg(video_identifier, temp_dir):
    
    # compressing the video
    print("compressing the video")
    compressed_path = os.path.join(temp_dir, 'compressed' + video_identifier + '.mp4')
    subprocess.call(f"ffmpeg.exe -i {uncompressed_path} -crf 30 {compressed_path}", shell=True)
    
    return;

main()

    
# todo learn how to use this in a discord bot setting
#fluentkopimist: When calling a function that returns a value, you need to store that in a variable. So, your line should be  value = check_working_directory()
# value can be any variable name you choose)