import urllib.request
import requests
import urllib.parse
import json

def load_twitch_ids():
    with open("twitch_json_example.json", "r") as read_file:
        file = json.load(read_file)

    return file

my_dict = load_twitch_ids()

CLIENT_ID = my_dict["client_id"]
CLIENT_SECRET = my_dict["client_secret"]


def make_request(URL):
    
    header = {"client-id": CLIENT_ID, "Authorization": f"Bearer {get_access_token()}"}

    req = urllib.request.Request(URL, headers=header)
    recv = urllib.request.urlopen(req)

    return json.loads(recv.read().decode("utf-8"))

def  get_access_token():
    x = requests.post(f"https://id.twitch.tv/oauth2/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type=client_credentials")

    return json.loads(x.text)["access_token"]

def get_current_online_streams():
    streamer = [
        "example1", #fill your list with the streamer names
        "example2"
    ]

    url = "https://api.twitch.tv/helix/streams?user_login="
    resps = []
    online_streams= []  

    for name in streamer:
        resps.append(make_request(url + name))

    print(resps)

    GAME_URL = "https://api.twitch.tv/helix/games?id="
    for i, r in enumerate(resps, 0):
        if r["data"]:
            game_id   = r["data"][0]["game_id"]
            game_resp = make_request(GAME_URL + game_id) 
            game_name = game_resp["data"][0]["name"]
            online_streams.append((streamer[i], game_name))
    
    print(online_streams)

def main():
    get_current_online_streams()



if __name__ == "__main__":
    main()