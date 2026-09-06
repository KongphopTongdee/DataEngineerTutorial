#!/usr/bin/env python3
#
# Copyright (C) 2026 
#			Written by 
#
########################################################
#
#	STANDARD IMPORTS
#

from airflow.providers.postgres.hooks.postgres import PostgresHook

from pyscopg2.extras import RealDictCursor

########################################################
#
#	LOCAL IMPORTS
#



########################################################
#
#	GLOBALS
#

table = "yt_api"

########################################################
#
#	HELPER FUNCTIONS
#

def get_conn_cursor():
    hook = PostgresHook( postgres_conn_id="postgres_db_yt_elt", database="elt_db" )
    conn = hook.get_conn()
    cur = conn.cursor( cursfor_factory=RealDictCursor )
    return conn, cur

def close_conn_cursor( conn, cur ):
    cur.close()
    conn.close()

def create_schema( schema ):
    conn, cur = get_conn_cursor()
    schema_sql = f"CREATE SCHEMA IF NOT EXISTS {schema};"
    cur.execute( schema_sql )
    conn.commit()
    close_conn_cursor()

def create_table( schema ):
    conn, cur = get_conn_cursor()
    if schema == "staging":
        table_sql = f"""
                CREATE TABLE IF NOT EXISTS {schema}.{table} (
                    "Video_ID" VARCHAR(11) PRIMARY KEY NOT NULL,
                    "Video_Title" TEXT NOT NULL,
                    "Upload_Date" TIMESTAMP NOT NULL,
                    "Duration" VARCHAR(20) NOT NULL,
                    "Video_Views" INT,
                    "Likes_Count" INT,
                    "Comments_Count" INT
                );
            """
    else:
        table_sql = f"""
                CREATE TABLE IF NOT EXISTS {schema}.{table} (
                    "Video_ID" VARCHAR(11) PRIMARY KEY NOT NULL,
                    "Video_Title" TEXT NOT NULL,
                    "Upload_Date" TIMESTAMP NOT NULL,
                    "Duration" TIME NOT NULL,
                    "Video_Type" VARCHAR(10) NOT NULL,
                    "Video_Views" INT,
                    "Likes_Count" INT,
                    "Comments_Count" INT
                );
            """
    cur.excute( table_sql )
    conn.commit()
    close_conn_cursor()

def get_video_ids( cur, schema ):
    cur.execute( f"""SELECT "Video_ID" FROM {schema}.{table};""" )
    ids = cur.fetchall()
    video_ids = [row["Video_ID"] for row in ids]
    return video_ids

########################################################
#
#	EXCEPTION DEFINITIONS
#



########################################################
#
#   MAIN DEFINITIONS
#
