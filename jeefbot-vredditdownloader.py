import requests
import sys
import os
import json
import subprocess
import ffmpeg


#This is a vredditdownloader function I am writing, to be implemented into a discord bot called "JeefBot" sometime in the future.



def main():
    
    #uncomment whichever reddit url needed for debug
    reddit_url = "https://old.reddit.com/r/aww/comments/kr98n2/the_corgi_express/"#example vreddit webm with no audio
    #reddit_url = "https://old.reddit.com/r/leagueoflegends/comments/88rypt/jesus_christ_if_this_gets_enough_upvotes_it_will/" #example reddit url containing no audio or video
    #reddit_url = "https://old.reddit.com/r/nextfuckinglevel/comments/kn8qs4/dont_touch_the_trash_can/" #example vreddit webm with audio
    #reddit_url = "https://old.reddit.com/r/Madrid/comments/hopsfy/theres_a_lot_to_be_said_but_i_just_cant/"
    #reddit_url = "https://old.reddit.com/r/PublicFreakout/comments/jgl8dn/most_polite_arrest_ever/"
    #reddit_url = "https://old.reddit.com/r/wallstreetbets/comments/l782pi/buy_gamestop_stock_wsb_pulled_from_twitter_the/"
    #reddit_url = "https://old.reddit.com/r/wallstreetbets/comments/lcjgc2/this_sub/"
    reddit_url = input("Reddit url: ")
    id = increment_video_id()
    
    download_vreddit_video(reddit_url) #==================================== Apparently you cant return multiple values. look into dictionaries maybe?

    #uncompressed_path = combine_with_ffmpeg()

    return 0
    
    

def increment_video_id():

    int(id) + 1
    
    return id;
        
def check_working_directory():
    
    #current_dir = os.getcwd() #gets program's current directory if you would like to use it that way, currently messed up because of the space in my username
    #current_dir = f'"{current_dir}"' #this was an attempt to fix by putting quotes around "current_dir" this didnt work either
    current_dir = "c:\jeefbot" #creates working directory in the c: drive where no spaces can get in my way
    working_dir = os.path.join(current_dir, r'vredditdownloader')
    if not os.path.exists(working_dir):
        os.makedirs(working_dir)
    
    return working_dir;

def download_vreddit_video(reddit_url):

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
        with open(os.path.join(working_dir ,'video_' + str(id) + '.mp4'), "wb") as f:
            for chunk in r.iter_content(chunk_size = 16*1024): #request file in chunks for speed and less ram usage
                f.write(chunk)
    except:
        print ("Something went wrong with the video request. probably bad url.")
    
    audio_url = r_dict[0]['data']['children'][0]['data']['url'] + "/DASH_audio.mp4" #the audio is stored at basically the same location and by appending /DASH_audio we can find it

    r = requests.get(audio_url, stream = True) #requesting audio from reddit
    with open(os.path.join(working_dir ,'audio_' + str(id) + '.mp4'), "wb") as f:
        for chunk in r.iter_content(chunk_size = 16*1024): #request file in chunks for speed and less ram usage
            f.write(chunk)
        
    b = os.path.getsize(os.path.join(working_dir ,'audio_' + str(id) + '.mp4')) #requests still manages to download mp3's when there arent any, this checks the size of the file and returns false if the file contains no data
    print (b)
    if b > 250:
        combine_with_ffmpeg()
        return
    else:
        print ("No audio found, this video probably doesnt contain any audio source.")
        os.remove(os.path.join(working_dir ,'audio_' + str(id) + '.mp4'))
        os.startfile('video_' + str(id) + '.mp4')
    
    return;

def combine_with_ffmpeg():
    
    # combining audio and video into one file
    print("Combining audio and video into one file")
    uncompressed_path = os.path.join(working_dir, 'uncompressed_' + str(id) + '.mp4')
    subprocess.call(f"ffmpeg.exe -hide_banner -loglevel fatal -i {os.path.join(working_dir ,'video_' + id + '.mp4')} -i {os.path.join(working_dir ,'audio_' + id + '.mp4')} -c copy {uncompressed_path}", shell=True)#quiet
    #subprocess.call(f"ffmpeg.exe -hide_banner -i {os.path.join(working_dir ,'video_' + id + '.mp4')} -i {os.path.join(working_dir ,'audio_' + id + '.mp4')} -c copy {uncompressed_path}", shell=True)#loud
    #for less verbosity use -hide_banner -loglevel fatal to only print fatal warnings
    print ("Saved at " + uncompressed_path ) 
    b = os.path.getsize(os.path.join(working_dir ,'video_' + str(id) + '.mp4')) #requests still manages to download mp3's when there arent any, this checks the size of the file and returns false if the file contains no data
    print (b)
    
    if b > 8000000:
        
        print ("Webm larger than 8 MB... Discord won't accept it without Nitro.")
        print("Jeef will compress it for you.")
        compress_with_ffmpeg(uncompressed_path)
        
        return uncompressed_path;
    else:

        print ("deleting extra files... ")
        os.remove(os.path.join(working_dir ,'audio_' + str(id) + '.mp4'))
        print ('audio_' + str(id) + '.mp4')
        os.remove(os.path.join(working_dir ,'video_' + str(id) + '.mp4'))
        print('video_' + str(id) + '.mp4')
        os.startfile(uncompressed_path)

        return;


def compress_with_ffmpeg(uncompressed_path):
    print ("Compressing...")
    b = os.path.getsize(os.path.join(working_dir ,'video_' + str(id) + '.mp4'))
    y = 0 
    i = 1
    while b >= 8000000 :
        
        print ("Current Pass: ", y, " ", b/1000000, "mb", end='\r')
        y += 1

        if y == 1 :
            compressed_path = os.path.join(working_dir ,'compressed_' + str(y) + '.mp4')
            subprocess.call(f"ffmpeg.exe -hide_banner -loglevel fatal -i {uncompressed_path} -crf 30 {compressed_path}", shell=True)#quiet
            #subprocess.call(f"ffmpeg.exe -hide_banner -i {uncompressed_path} -crf 30 {compressed_path}", shell=True)#loud
            b = os.path.getsize(os.path.join(working_dir ,'compressed_' + str(y) + '.mp4'))
            old_compressed_path = compressed_path
            
            #print (b, " routine 1 ", y) #debug
        
        else:
            old_compressed_path = compressed_path
            compressed_path = os.path.join(working_dir ,'compressed_' + str(y) + '.mp4')
            subprocess.call(f"ffmpeg.exe -hide_banner -loglevel fatal -i {old_compressed_path} -crf 30 {compressed_path}", shell=True)#quiet
            b = os.path.getsize(os.path.join(working_dir ,'compressed_' + str(y) + '.mp4'))
            
            #print (b, " routine 2 ", y) #debug
            
    print("compression successful, saved at " + compressed_path)
    print ("completed in ", y ,"passes")
        
    print ("deleting extra files...")

    os.remove(os.path.join(working_dir ,'uncompressed_' + str(id) + '.mp4'))
    while i < y:
        os.remove(os.path.join(working_dir ,'compressed_' + str(i) + '.mp4'))
        print ('compressed_' + str(i) + '.mp4')
        i += 1
            
    os.remove(os.path.join(working_dir ,'audio_' + str(id) + '.mp4'))
    print ('audio_' + str(id) + '.mp4')
    os.remove(os.path.join(working_dir ,'video_' + str(id) + '.mp4'))
    print('video_' + str(id) + '.mp4')
    
    os.startfile(compressed_path)
    
    


global id
id = "0"

global working_dir
working_dir = check_working_directory()

global uncompressed_path
main()

    
# todo learn how to use this in a discord bot setting
# When calling a function that returns a value, you need to store that in a variable. So, your line should be  value = check_working_directory()
# value can be any variable name you choose)