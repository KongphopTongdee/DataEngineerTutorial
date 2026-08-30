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

url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"

########################################################
#
#	HELPER FUNCTIONS
#

def convertPythonToJson( data ):
    dataToJson = data.json()
    answer = json.dumps( dataToJson, indent=4 )
    return answer

def get_playlist_ID():
    try:
        responseData = requests.get( url )
        responseData.raise_for_status()

        dataJson = responseData.json()

        jsonData = convertPythonToJson( responseData )
        # print( "jsonData",jsonData )

        # Get the output from the json
        channel_items = dataJson["items"][0]
        channel_playlistID = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        print( channel_playlistID )
        return channel_playlistID
    except requests.exceptions.RequestException as e:
        raise e


########################################################
#
#	EXCEPTION DEFINITIONS
#



########################################################
#
#   MAIN DEFINITIONS
#

def main():
    get_playlist_ID()

if __name__ == '__main__':
    main()