import csv, sys, os, requests, json
from datetime import datetime

# $1 param is fps
# $2 length to record
# $3 slowdown


print(sys.argv[1])
if sys.argv[1] == '90':
    print("Recording at 90fps")
    os.system("raspivid -t " + str(sys.argv[2]) + " -ex fixedfps -o /home/pi/projekt/90fps.h264")
    os.system("MP4Box -add 90fps.h264 90fps.mp4")
    #Get the info from the uploaded config-video.json file
    today = datetime.today()
    finalFileName = "";
    finalFileName += today.strftime("%d-%m-%Y-%H%M")
    with open('config-video.json') as json_file:
        data = json.load(json_file)
        finalFileName += "-" + "90"
        finalFileName += "-" + str(data["length"])
        finalFileName += "-" + "0"
        finalFileName += "-" + str(data["name"])

    finalFileName+=".mp4"
    print(finalFileName)
    os.rename("90fps.mp4", finalFileName)
    #Upload to master
    files = {'video': open(finalFileName, 'rb')}
    response = requests.post("http://192.168.0.103:3000/api/uploadvideo", files=files)
    response.text
else:
    print("Recording at 660fps")
    os.system("rm -r /opt/temp/*tiff")
    os.system("rm -r /opt/temp/*raw")
    os.system("rm -r /opt/temp/output.mp4")
    os.system("rm -r /opt/temp/*all")
    os.system("rm -r /opt/temp/ffmpeg_concats.txt")
    os.system("rm -r -f /opt/temp/*")
    os.system("/home/pi/fork-raspiraw/camera_i2c")
    os.system("/home/pi/fork-raspiraw/raspiraw -md 7 -t " + sys.argv[2] + " -ts /opt/temp/tstamps.csv -hd0 /opt/temp/hd0.32k -h 128 -w 640 --vinc 1F --fps " + sys.argv[1] + " -sr 1 -o /opt/temp/out.%06d.raw")
    os.system('ls /opt/temp/*.raw | while read i; do cat /opt/temp/hd0.32k "$i" > "$i".all; done')
    os.system('ls /opt/temp/*.all | while read i; do /home/pi/dcraw/dcraw -f -o 1 -v  -6 -T -q 3 -W "$i"; done')

    os.system("python /home/pi/projekt/make_concat.py " + sys.argv[3] + " > /opt/temp/ffmpeg_concats.txt")
    os.system('ffmpeg -f concat -safe 0 -i /opt/temp/ffmpeg_concats.txt -vcodec libx265 -x265-params lossless -crf 0 -b:v 1M -pix_fmt yuv420p -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" /opt/temp/output.mp4')

    #Get the info from the uploaded config-video.json file
    today = datetime.today()
    finalFileName = "";
    finalFileName += today.strftime("%d-%m-%Y-%H%M")
    with open('config-video.json') as json_file:
        data = json.load(json_file)
        finalFileName += "-" + str(data["fps"])
        finalFileName += "-" + str(data["length"])
        finalFileName += "-" + str(data["slowdown"])
        finalFileName += "-" + str(data["name"])

    finalFileName+=".mp4"
    print(finalFileName)

    #Convert to h264, and rename file
    os.system("ffmpeg -i /opt/temp/output.mp4 -an -vcodec libx264 -crf 23 " + finalFileName)

    #Upload to master
    files = {'video': open(finalFileName, 'rb')}
    response = requests.post("http://192.168.0.103:3000/api/uploadvideo", files=files)
    response.text
