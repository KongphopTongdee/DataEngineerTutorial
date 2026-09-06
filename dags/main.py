#!/usr/bin/env python3
#
# Copyright (C) 2026 
#			Written by 
#
########################################################
#
#	STANDARD IMPORTS
#

from airflow import DAG

import pendulum

from datetime import datetime, timedelta

########################################################
#
#	LOCAL IMPORTS
#

from api.video_stats import get_playlist_ID, get_video_ids, extract_video_data, save_to_json


########################################################
#
#	GLOBALS
#

# Define the local timezone
local_tz = pendulum.timezone("Asia/Bangkok")

# Default Args
default_args = {
    "owner": "dataengineers",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "data@engineers.com",
    # 'retries': 1,
    # 'retry_delay': timedelta(minutes=5),
    "max_active_runs": 1,
    "dagrun_timeout": timedelta(hours=1),
    "start_date": datetime(2026, 9, 6, tzinfo=local_tz),
    # 'end_date': datetime(2030, 12, 31, tzinfo=local_tz),
}

########################################################
#
#	HELPER FUNCTIONS
#



########################################################
#
#	EXCEPTION DEFINITIONS
#



########################################################
#
#   MAIN DEFINITIONS
#

with DAG(
    dag_id="produce_json",
    default_args = default_args,
    description = "DAG to produce JSON file with raw data",
    schedule="0 14 * * *",
    catchup=False
) as dag:

    # Define tasks
    playlist_id = get_playlist_ID()
    video_ids = get_video_ids( playlist_id )
    extract_data = extract_video_data( video_ids )
    save_to_json_task = save_to_json( extract_data )

    # Define dependencies
    playlist_id >> video_ids >> extract_data >> save_to_json_task
