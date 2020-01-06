import requests
video = {'files[]': open('output.mp4', 'rb')}
response = requests.post("http://SERVERIP:3000/api/uploadvideo", files=files)
response.text
