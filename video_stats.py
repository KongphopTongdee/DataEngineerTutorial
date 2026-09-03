#!/usr/bin/env python3
#
# Copyright (C) 2026 
#			Written by 
#
########################################################
#
#	STANDARD IMPORTS
#

import requests

import json

import os 

from dotenv import load_dotenv

from datetime import date

########################################################
#
#	LOCAL IMPORTS
#

load_dotenv(dotenv_path="./.env")

########################################################
#
#	GLOBALS
#

API_KEY = os.getenv("API_KEY")

CHANNEL_HANDLE = "MrBeast"

maxResult = 50

########################################################
#
#	HELPER FUNCTIONS
#

def convertPythonToJson( data ):
    dataToJson = data.json()
    answer = json.dumps( dataToJson, indent=4 )
    return answer

def get_playlist_ID():
    url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"

    try:
        responseData = requests.get( url )
        responseData.raise_for_status()

        dataJson = responseData.json()

        jsonData = convertPythonToJson( responseData )
        # print( "jsonData",jsonData )

        # Get the output from the json
        channel_items = dataJson["items"][0]
        channel_playlistID = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        # print( channel_playlistID )
        return channel_playlistID
    except requests.exceptions.RequestException as e:
        raise e
 
def get_video_ids( playlistID ):
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResult}&playlistId={ playlistID }&key={API_KEY}"

    pageToken = None

    video_ids =[]

    try:

        while True :
            url = base_url

            if pageToken:
                url += f"&pageToken={pageToken}"

            responseData = requests.get( url )
            responseData.raise_for_status()
    
            dataJson = responseData.json()

            for item in dataJson.get( "items", [] ):
                video_id = item["contentDetails"]["videoId"]
                video_ids.append( video_id )

            pageToken = dataJson.get("nextPageToken")

            if not pageToken:
                break

        return video_ids  

    except requests.exceptions.RequestException as e:
        raise e

def extract_video_data( video_ids ):
    extracted_data = []

    def batch_list( video_id_lst, batch_size ):
        for video_id in range( 0, len( video_id_lst ), batch_size ):
            # Explain yield function in the goodnote
            yield video_id_lst[ video_id: video_id + batch_size ]

    try:
        for batch in batch_list( video_ids, maxResult ):
            video_ids_str = ",".join(batch)

            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}"

            responseData = requests.get( url )
            responseData.raise_for_status()
    
            dataJson = responseData.json()

            # Get the output in the json format
            for item in dataJson.get("items", []):
                video_id = item["id"]
                snippet = item[ "snippet" ]
                contentDetails = item["contentDetails"] 
                statistics = item["statistics"]

                # Create new data to easy understand on my own
                video_data = {
                    "video_id": video_id, 
                    "title": snippet["title"],
                    "publishedAt": snippet["publishedAt"],
                    "duration": contentDetails["duration"],
                    "viewCount": statistics.get("viewCount", None),
                    "likeCount": statistics.get("likeCount", None),
                    "commentCount": statistics.get("commentCount", None)
                }

                extracted_data.append( video_data )

        return extracted_data
        
    except requests.exceptions.RequestException as e:
        raise e

def save_to_json( extracted_data ):
    file_path = f"./data/YT_data_{date.today()}.json"

    with open( file_path, "w", encoding="utf-8" ) as json_outfile:
        json.dump( extracted_data, json_outfile, indent=4, ensure_ascii=False )

########################################################
#
#	EXCEPTION DEFINITIONS
#



########################################################
#
#   MAIN DEFINITIONS
#

def main():
    playlistID = get_playlist_ID()
    videoIDs = get_video_ids( playlistID )
    video_data = extract_video_data( videoIDs )
    save_to_json( video_data )

if __name__ == '__main__':
    main()