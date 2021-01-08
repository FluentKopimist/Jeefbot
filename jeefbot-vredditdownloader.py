import requests
import os
import json
import subprocess
import ffmpeg

#This is a vredditdownloader function I am writing, to be implemented into a discord bot called "JeefBot" sometime in the future.

def main():
    
    
    #uncomment whichever reddit url needed for debug
    #reddit_url = "https://old.reddit.com/r/aww/comments/kr98n2/the_corgi_express/"#example vreddit webm with no audio
    #reddit_url = "https://old.reddit.com/r/leagueoflegends/comments/88rypt/jesus_christ_if_this_gets_enough_upvotes_it_will/" #example reddit url containing no audio or video
    reddit_url = "https://old.reddit.com/r/nextfuckinglevel/comments/kn8qs4/dont_touch_the_trash_can/" #example vreddit webm with audio
    
    vid_id = vid_id + 1; #vid_id will be a global variable that will increment by 1 every time this is ran, identifying the videos and the audio that goes with it

    working_dir = check_working_directory()
    
    audio_flag = download_vreddit_video(working_dir, reddit_url, vid_id) #==================================== Apparently you cant return multiple values. look into dictionaries maybe?
    
    if audio_flag == true:
        combine_with_ffmpeg(working_dir, vid_id)
    
    if compress == true:
        compress_with_ffmpeg(working_dir, vid_id)
        
def check_working_directory():

    #current_dir = os.getcwd() #gets program's current directory if you would like to use it that way, currently messed up because of the space in my username
    #current_dir = f'"{current_dir}"' #this was an attempt to fix by putting quotes around "current_dir" this didnt work either
    current_dir = "c:\jeefbot" #creates working directory in the c: drive where no spaces can get in my way
    working_dir = os.path.join(current_dir, r'vredditdownloader')
    if not os.path.exists(working_dir):
        os.makedirs(working_dir)
    
    return working_dir;

def download_vreddit_video(working_dir, reddit_url vid_id):

    json_url = reddit_url + ".json"
    r = requests.get(json_url, headers={'User-agent': 'JeefBot'}) #connect to reddit using fake user agent so it doesn't kick us out for avoiding their api
    r_dict = json.loads(r.text) #creates dictionary file with our json so we may query it for the values we need

    try:
        video_url = r_dict[0]['data']['children'][0]['data']['secure_media']['reddit_video']['fallback_url'] #filter .json for video url
        print ("Found video url at: ", video_url)
       
        
    except:
        print ("As far as I can tell the url at:")
        print (reddit_url) 
        print ("Does not contain any video source.") #-------------------------------------------log it instead of print
        exit()
          
    try:
        r = requests.get(video_url, stream = True) #requesting video from reddit
        with open(os.path.join(working_dir ,'video' + vid_id + '.mp4'), "wb") as f:
            for chunk in r.iter_content(chunk_size = 16*1024): #request file in chunks for speed and less ram usage
                f.write(chunk)
    except:
        print ("Something went wrong with the video request. probably bad url.")
    
    audio_url = r_dict[0]['data']['children'][0]['data']['url'] + "/DASH_audio.mp4" #the audio is stored at basically the same location and by appending /DASH_audio we can find it

    try:
        r = requests.get(audio_url, stream = True) #requesting audio from reddit
        with open(os.path.join(working_dir ,'audio' + vid_id + '.mp4'), "wb") as f:
            for chunk in r.iter_content(chunk_size = 16*1024): #request file in chunks for speed and less ram usage
                f.write(chunk)
        audio_flag = true
    except:
        print ("No audio found, this video probably doesnt contain any audio source.")
        audio_flag = false
    
    
    return audio_flag;

def combine_with_ffmpeg(working_dir, vid_id):

     # combining audio and video into one file
    print("combining audio and video into one file")
    uncompressed_path = os.path.join(working_dir, 'uncompressed' + vid_id + '.mp4')
    subprocess.call(f"ffmpeg.exe -hide_banner -loglevel fatal -i {os.path.join(working_dir ,'video' + vid_id + '.mp4')} -i {os.path.join(working_dir ,'audio' + vid_id + '.mp4')} -c copy {uncompressed_path}", shell=True)
    print ("Saved at " + uncompressed_path ) # for less verbosity use -hide_banner -loglevel fatal to only print fatal warnings
    return;

def compress_with_ffmpeg(working_dir, vid_id):
    
    # compressing the video
    print("compressing the video")
    compressed_path = os.path.join(working_dir, 'compressed' + vid_id + '.mp4')
    subprocess.call(f"ffmpeg.exe -hide_banner -loglevel fatal -i {uncompressed_path} -crf 30 {compressed_path}", shell=True)
    print("compression successful, saved at " + uncompressed_path  )
    
    
    return;

main()

    
# todo learn how to use this in a discord bot setting
# When calling a function that returns a value, you need to store that in a variable. So, your line should be  value = check_working_directory()
# value can be any variable name you choose)