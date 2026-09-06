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

########################################################
#
#	EXCEPTION DEFINITIONS
#



########################################################
#
#   MAIN DEFINITIONS
#
