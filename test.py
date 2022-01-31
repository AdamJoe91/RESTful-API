import requests

BASE = "http://127.0.0.1:5000/"#location of target URL
data = [{"likes":10000,"name":"Pog Moment","views":1000000},
        {"likes":1,"name":"Tutorial","views":1000},
        {"likes":0,"name":"Garbage","views":1}]
        
        
for i in range(len(data)):

    response = requests.put(BASE + "video/"+str(i),data[i])

    print(response.json())

input()
response = requests.get(BASE + "video/6")
print(response.json())