# youtube data harvesting
import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
import pymongo
import mysql.connector
import pandas as pd
import re

API_KEY = 'AIzaSyABS0BI5sgoNlVmf1r85Bk7rf1hk1eA7sU'


def get_channel_data(channel_id):
    all_data = []
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    channel_response = youtube.channels().list(
        part='snippet,contentDetails,statistics',
        id=channel_id
    ).execute()

    for item in channel_response['items']:
        data = {
            'Channel Name': item['snippet']['title'],
            'Channel Description': item['snippet']['description'],
            'Subscriber Count': item['statistics']['subscriberCount'],
            'View Count': item['statistics']['viewCount'],
            'Video Count': item['statistics']['videoCount']
        }

        if 'contentDetails' in item:
            data['Playlist ID'] = item['contentDetails'].get('relatedPlaylists', {}).get('uploads')
            data['Playlist NAME'] = item['contentDetails'].get('relatedPlaylists', {}).get('uploads')

        all_data.append(data)

    return all_data


def get_video_ids(youtube, playlist_id):
    video_ids = []
    request = youtube.playlistItems().list(
        part='snippet,contentDetails',
        playlistId=playlist_id,
        maxResults=50
    )
    response = request.execute()
    for item in response['items']:
        video_ids.append(item['contentDetails']['videoId'])
    next_page_token = response.get("nextPageToken")

    while next_page_token:
        request = youtube.playlistItems().list(
            part='snippet,contentDetails',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])
        next_page_token = response.get("nextPageToken")

    return video_ids


def get_video_details(youtube, video_ids):
    all_video_status = []
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part='snippet,statistics,contentDetails',
            id=','.join(video_ids[i:i + 50])
        )
        response = request.execute()
        for video in response['items']:
            video_info = {
                'Video_Id': video['id'],
                'Video_Title': video['snippet']['title'],
                'Video_Description': video['snippet']['description'],
                'Tags': video['snippet'].get('tags', []),
                'Published_At': video['snippet']['publishedAt'],
                'View_Count': video['statistics']['viewCount'],
                'Like_Count': video['statistics']['likeCount'],
                'Dislike_Count': video['statistics'].get('dislikeCount', 0),
                'Favorite_Count': video['statistics']['favoriteCount'],
                'Comment_Count': video['statistics'].get('commentCount', 0),
                'Duration': video['contentDetails']['duration'],
                'Thumbnail': video['snippet']['thumbnails']['default']['url'],
                'Caption_Status': video['contentDetails']['caption']
            }
            all_video_status.append(video_info)
    return all_video_status


def get_comment_in_video(youtube, video_ids):
    all_comments = []

    for video_id in video_ids:
        try:
            request = youtube.commentThreads().list(
                part="snippet,replies",
                videoId=video_id,
                maxResults=20
            )
            response = request.execute()

            for comment in response['items']:
                get_comments_in_videos = {
                    "comment_id": comment["snippet"]["topLevelComment"]["id"],
                    "comment_text": comment["snippet"]["topLevelComment"]["snippet"]["textDisplay"],
                    "comment_author": comment["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                    "comment_publishedAt": comment["snippet"]["topLevelComment"]["snippet"]["publishedAt"],
                    "video_id": comment["snippet"]["videoId"]
                }
                all_comments.append(get_comments_in_videos)

        except HttpError as e:
            if e.resp.status == 404:
                print(f"Video not found for video ID: {video_id}")
            else:
                pass

    return all_comments

st.tittle=('YouTube Data Harvesting')

channel_id = ['UCQYO2p7JMcCp-9xIZxGP2Sg', 'UCXhbCCZAG4GlaBLm80ZL-iA', 'UC9trsD1jCTXXtN3xIOIU8gg',
              'UCoCG7wgXEBOfyTfeFylzIaw', 'UCniI-BQk7qAtXNmmz40LSdg', 'UCzee67JnEcuvjErRyWP3GpQ',
              'UCYXVX9Iwupv0M-aSrxUHCXQ', 'UCa9c6LDV43ZfD89zsxkEyzg', 'UCtcTNRfGeHcHxEXKSUu84Fw',
              'UCBnxEdpoZwstJqC1yZpOjRA']

selected_channel_id = st.selectbox('Select Channel ID:', channel_id)
transfer = st.button('Extract')

if transfer:
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    channel_data = get_channel_data(selected_channel_id)
    st.write(channel_data)

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['youtube']
    collection = db['channel_data']
    collection.insert_many(channel_data)

    playlist_id = channel_data[0].get('Playlist ID')
    if playlist_id:
        video_ids = get_video_ids(youtube, playlist_id)
        vid_details = get_video_details(youtube, video_ids)
        collection = db['video_details']
        collection.insert_many(vid_details)
        st.write(vid_details)




        # for video_id in video_ids:
        comment_data = get_comment_in_video(youtube, video_ids)

        if comment_data:  # Check if comment_data is not empty
            collection = db['comment_data']
            collection.insert_many(comment_data)
            st.write(comment_data)
        else:
            st.write("No comments found for video:", video_id)
mysql_db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Gobi@7819",
        database="youtube"
        )
mysql_cursor = mysql_db.cursor()

load=st.button('load')
if load:
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    mongo_db = mongo_client['youtube']
    mongo_collection = mongo_db['channel_data']
    mongo_data = mongo_collection.find({})

    for data in mongo_data:
        # Assuming you have fields 'field1', 'field2', and 'field3' in your MongoDB collection
        channel_id = selected_channel_id
        channel_name = data["Channel Name"]
        channel_view = data["View Count"]
        channel_description = data["Channel Description"]



        # Assuming you have corresponding columns 'field1', 'field2', and 'field3' in your MySQL table
        sql = "INSERT INTO channel (channel_id, channel_name, channel_view, channel_description) VALUES (%s, %s, %s, %s)"
        values = (channel_id, channel_name, channel_view, channel_description)

        # Execute the SQL statement
        mysql_cursor.execute(sql, values)
        # mysql_cursor.execute(values)

    mongo_video=mongo_db['video_details']
    mongo_video_data=mongo_video.find({})
    for videodata in mongo_video_data:
        video_id = videodata[ "Video_Id"]
        playlist_id = data["Playlist ID"]
        video_name = videodata[ "Video_Title"]
        video_descrption = videodata[ "Video_Description"]
        published_date = videodata[ "Published_At"]
        published_date = datetime.datetime.strptime(published_date, '%Y-%m-%dT%H:%M:%SZ')
        formatted_published_date = published_date.strftime('%Y-%m-%d %H:%M:%S')
        view_count = videodata[ "View_Count"]
        like_count = videodata[ "Like_Count"]
        dislike_count = videodata[ "Dislike_Count"]
        favorite_count = videodata[ "Favorite_Count"]
        comment_count = videodata[ "Comment_Count"]
        duration = videodata[ "Duration"]
        minutes_match = re.search(r'(\d+)M', duration)
        seconds_match = re.search(r'(\d+)S', duration)

        minutes = int(minutes_match.group(1)) if minutes_match else 0
        seconds = int(seconds_match.group(1)) if seconds_match else 0

        duration = minutes * 60 + seconds


        thumbnail = videodata[ "Thumbnail"]
        caption_status = videodata[ "Caption_Status"]

        sql = "INSERT INTO video (video_id, playlist_id, video_name, video_descrption, published_date, view_count, like_count, dislike_count, favorite_count, comment_count, duration, thumbnail, caption_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (video_id , playlist_id , video_name , video_descrption, published_date, view_count, like_count, dislike_count, favorite_count, comment_count, duration, thumbnail, caption_status)

        mysql_cursor.execute(sql, values)

    mongo_comment = mongo_db['comment_data']
    mongo_comment_data = mongo_comment.find({})
    for commentdata in mongo_comment_data:
        comment_id = commentdata["comment_id"]
        video_id = commentdata["video_id"]
        comment_text = commentdata["comment_text"]
        comment_author = commentdata["comment_author"]
        comment_published_date = commentdata["comment_publishedAt"]
        comment_published_date = datetime.datetime.strptime(comment_published_date, '%Y-%m-%dT%H:%M:%SZ')
        comment_published_date = comment_published_date.strftime('%Y-%m-%d %H:%M:%S')

        sql = "INSERT INTO comment(comment_id, video_id, comment_text, comment_author, comment_published_date) values ( %s, %s, %s, %s, %s)"
        values = (comment_id, video_id, comment_text, comment_author, comment_published_date)

        mysql_cursor.execute(sql, values)

        playlist_name = data["Playlist NAME"],
        playlist_id = data["Playlist ID"],
        channel_id = selected_channel_id

        sql = "INSERT INTO playlist(playlist_id, channel_id, playlist_name) values (%s, %s, %s)"
        values = (playlist_id[0], channel_id, playlist_name[0])
        st.write(values)
        mysql_cursor.execute(sql, values)
        break



    # Commit the changes to MySQL
mysql_db.commit()


    # Close the connections
# mongo_client.close()
# mysql_cursor.close()
# mysql_db.close()
question=['SELECT a.video_name, b.channel_name FROM video a JOIN playlist c ON a.playlist_id = c.playlist_id JOIN channel b ON c.channel_id = b.channel_id;'
    ,'SELECT channel_name, COUNT(*) AS video_count FROM video JOIN channel ON video.playlist_id = channel.channel_id GROUP BY channel_name ORDER BY video_count DESC;'
          ,'SELECT video.video_name, channel.channel_name, video.view_count FROM video JOIN channel ON video.playlist_id = channel.channel_id ORDER BY video.view_count DESC LIMIT 10;'
           ,'SELECT video.video_name, COUNT(comment.comment_id) AS comment_count FROM video LEFT JOIN comment ON video.video_id = comment.video_id GROUP BY video.video_id, video.video_name;'
           , 'SELECT video.video_name, channel.channel_name, video.like_count FROM video INNER JOIN channel ON video.playlist_id_id = channel.channel_id WHERE video.likes = (SELECT MAX(like_count) FROM video);'
            ,'SELECT video.video_name, SUM(video.like_count) AS total_likes, SUM(video.dislike_count) AS total_dislikes FROM video GROUP BY video.video_name;'
            ,'SELECT channel.channel_name, SUM(video.view_count) AS total_views FROM channel JOIN video ON channel.channel_id = video.playlist_id GROUP BY channel.channel_name;'
             ,'SELECT DISTINCT channel.channel_name FROM channel JOIN video ON channel.channel_id = video.playlist_id WHERE YEAR(video.publish_date) = 2022;'
              ,'SELECT channel.channel_name, AVG(video.duration) AS average_duration FROM channel JOIN video ON channel.channel_id = video.playlist_id GROUP BY channel.channel_name;'
              ,'SELECT video.video_name, channel.channel_name, COUNT(comment.comment_id) AS comment_count FROM video JOIN channel ON video.playlist_id = channel.channel_id JOIN comment ON video.video_id = comment.video_id GROUP BY video.video_id ORDER BY comment_count DESC LIMIT 10;']
query=st.selectbox('select query :', question)
if query:
    # st.write(query)
    load_data=mysql_cursor.execute(query)
    result = mysql_cursor.fetchall()
    st.write(result)
    df = pd.DataFrame(result, columns=["Video Name", "Channel Name", 'total_like'])
    st.write(df)