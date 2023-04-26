import os
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime

# Replace 'YOUR_API_KEY' with your actual API key
API_KEY = 'My API Key'

# Create a YouTube Data API service
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Specify the parameters for the API request
request = youtube.search().list(
    part='id',
    type='channel',
    q='MrBeast'  # Replace with the name or keyword of the YouTube channel
)

# Execute the API request and retrieve the response
response = request.execute()

# Extract the channel ID from the API response
channel_id = response['items'][0]['id']['channelId']


# Retrieve the list of videos from the channel
def get_channel_videos(channel_id):
    videos = []
    next_page_token = None
    while True:
        response = youtube.search().list(
            part='id,snippet',  # Include snippet in part parameter
            type='video',
            channelId=channel_id,
            maxResults=50,  # Adjust this value as needed
            pageToken=next_page_token
        ).execute()
        videos += response['items']
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    return videos

# Retrieve video analytics for each video
def get_video_analytics(video_id):
    response = youtube.videos().list(
        part='statistics',
        id=video_id
    ).execute()
    return response

# Retrieve video information for each video
def get_video_info(video_id):
    response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()
    return response

# Retrieve content details for each video
def get_video_content_details(video_id):
    response = youtube.videos().list(
        part='contentDetails',
        id=video_id
    ).execute()
    return response

# Retrieve video analytics, information, and content details for all videos in the channel
def get_all_video_data(channel_id):
    videos = get_channel_videos(channel_id)
    video_data = []
    for video in videos:
        video_id = video['id']['videoId']
        analytics = get_video_analytics(video_id)
        info = get_video_info(video_id)
        content_details = get_video_content_details(video_id)
        video_data.append({
            'videoId': video_id,
            'title': info['items'][0]['snippet'].get('title',''),
            'description': info['items'][0]['snippet'].get('description'),
            'publishedAt': info['items'][0]['snippet'].get('publishedAt',''),
            'viewCount': analytics['items'][0]['statistics'].get('viewCount',''),
            'likeCount': analytics['items'][0]['statistics'].get('likeCount',''),
            'commentCount': analytics['items'][0]['statistics'].get('commentCount',''),
            'duration': content_details['items'][0]['contentDetails'].get('duration','')
        })
    return video_data

# Save video data in a Pandas dataframe
def save_video_data_to_dataframe(video_data):
    df = pd.DataFrame(video_data)
    return df

# Call the functions to retrieve video data and save to dataframe
video_data = get_all_video_data(channel_id)
df = save_video_data_to_dataframe(video_data)

# Call the playlists.list API endpoint to retrieve the playlists for the channel
try:
    playlists = []
    next_page_token = ''
    while next_page_token is not None:
        playlists_request = youtube.playlists().list(
            part='id',
            channelId=channel_id,
            maxResults=50,  # You can adjust this to retrieve more or fewer playlists per request
            pageToken=next_page_token
        )
        playlists_response = playlists_request.execute()
        playlists.extend(playlists_response.get('items', []))
        next_page_token = playlists_response.get('nextPageToken')
except HttpError as e:
    print(f'An error occurred: {e}')
    playlists = None

# Extract the playlist IDs from the playlist items
if playlists is not None:
    playlist_ids = [playlist['id'] for playlist in playlists]


def get_all_playlist_videos(playlist_ids):
    videos = []
    next_page_token = None
    for playlist_id in playlist_ids:
        while True:
            response = youtube.playlistItems().list(
                part='id,snippet',
                playlistId=playlist_id,
                maxResults=100,  # Increase this value to retrieve more results per page
                pageToken=next_page_token
            ).execute()
            for item in response['items']:
                video_id = item['snippet']['resourceId']['videoId']
                videos.append({'videoId': video_id, 'snippet': item['snippet']})
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
    return videos


def get_all_video_data(playlist_ids):
    videos = get_all_playlist_videos(playlist_ids)
    video_data = []
    for video in videos:
        video_id = video['videoId']
        analytics = get_video_analytics(video_id)
        info = get_video_info(video_id)
        content_details = get_video_content_details(video_id)
        video_data.append({
            'videoId': video_id,
            'title': info['items'][0]['snippet'].get('title',''),
            'description': info['items'][0]['snippet'].get('description'),
            'publishedAt': info['items'][0]['snippet'].get('publishedAt',''),
            'viewCount': analytics['items'][0]['statistics'].get('viewCount',''),
            'likeCount': analytics['items'][0]['statistics'].get('likeCount',''),
            'commentCount': analytics['items'][0]['statistics'].get('commentCount',''),
            'duration': content_details['items'][0]['contentDetails'].get('duration','')
        })
    return video_data

video_data = get_all_video_data(playlist_ids)
df_2 = save_video_data_to_dataframe(video_data)



final_df = pd.concat([df, df_2], axis=0)



def convert_duration_to_seconds(duration):
    # Extract the hours, minutes, and seconds from the duration string
    hours = 0
    minutes = 0
    seconds = 0

    if 'H' in duration:
        hours = int(duration.split('H')[0][2:])
        duration = duration.split('H')[1]
    if 'M' in duration:
        minutes = duration.split('M')[0][2:]
        if minutes!="":
            minutes=int(minutes)
        else:
            minutes=0
        duration = duration.split('M')[1]
    if 'S' in duration and 'M' not in duration:
        seconds = int(duration[-3:-1])
    elif 'S' in duration and 'M' in duration:
        seconds = int(duration.split('S')[0])

    # Calculate the total duration in seconds
    total_seconds = hours * 3600 + minutes * 60 + seconds
    #print(hours,minutes,seconds)
    return total_seconds


final_df['duration'] = final_df['duration'].apply(convert_duration_to_seconds)

# drop duplicates from final_df based on title 
# The reason to drop them is because we are using two functions to get the data: get_all_video_data and get_all_playlist_videos
# The two functions will get the same video twice, so we need to drop the duplicates
# In this project, the I have dropped the duplicates in the RMD file instead of here
# final_df = final_df.drop_duplicates(subset=['title'], keep='first')

final_df.to_csv(r"MrBeastYoutube.csv")
