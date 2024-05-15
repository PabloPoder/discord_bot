import requests
# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth

# # Initialize Spotipy with client credentials
# client_id = '217cae14211c4989b93a873e3b845875'
# client_secret = '94d9c4e00ef8493ba7c1b3ef5f030f5f'
# client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

# Authorization token obtenido previamente
token = 'BQCfwsJHRk829t6fWG1xH-1aGk3qF1CFAd6zWrQuQkREDlKPRKJJ7ZBI4Df_VSEALrFDwNzEjvI425VK52-NRCCkti_4oXd-5sVddegaHWZMoNDnws_SGTW1FICWErHYccFVTXw8Vvf48001qe9iubuU5akzo8Ur6bpnAXsa7a3a1rTmY4pi12dDALanZnq6xPmwi-QLfKBoX-kZ_A8J-pJD6P73quVAqIiuNNPuH6CksugVLY6dLg3MXnGLHgkZMpSvXg'

def fetch_web_api(endpoint, method, body=None):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    url = f'https://api.spotify.com/{endpoint}'
    response = requests.request(method, url, headers=headers, json=body)
    return response.json()

async def get_top_tracks():
    # Referencia del endpoint: https://developer.spotify.com/documentation/web-api/reference/get-users-top-artists-and-tracks
    response = await fetch_web_api('v1/me/top/tracks?time_range=long_term&limit=5', 'GET')
    return response.get('items', [])

top_tracks = get_top_tracks()
for track in top_tracks:
    artists = ', '.join([artist['name'] for artist in track['artists']])
    print(f"{track['name']} by {artists}")