import sqlite3
import json
import os
import logging
import pprint

DATA_DIR = "data"
PROC_DATA_DIR = "processed_data"

logger = logging.getLogger("data_proc_logger")

formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

fileHandler = logging.FileHandler('log/process_data.log')
fileHandler.setFormatter(formatter)
streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)

logger.addHandler(fileHandler)
logger.addHandler(streamHandler)

fileHandler.setLevel(logging.DEBUG)
streamHandler.setLevel(logging.INFO)

logger.setLevel(logging.DEBUG)

conn = sqlite3.connect("./processed_data/insta_user_relations.sqlite3")


def extract_json_to_db(id, files):
    logger.info("%s : load json files --> %s" % (id, files))
    count = 0

    cur = conn.cursor()
    for file in files:
        with open(file) as data_file:
            data = json.load(data_file)
            for node in data["data"]["user"]["edge_follow"]["edges"]:
                cur.execute(
                    "INSERT OR REPLACE INTO users (id, username, full_name, profile_pic_url) VALUES ( %s, '%s', '%s', '%s' )"
                    %
                    (
                        node["node"]["id"],
                        node["node"]["username"],
                        str(node["node"]["full_name"]).replace("'", "''"),
                        node["node"]["profile_pic_url"]
                    ))
                cur.execute(
                    "INSERT OR IGNORE INTO relations (user_id,follow_id) VALUES ( %s, %s )" % (id, node["node"]["id"]))
                count = count + 1
    conn.commit()
    logger.info("%d users were added." % count)


dirs = [dir4id for dir4id in os.listdir('data') if os.path.isdir(os.path.join('data', dir4id))]

target_ids = []

cur = conn.cursor()
for a_dir in dirs:
    end_file = os.path.join(DATA_DIR, os.path.join(a_dir, 'END'))
    if os.path.exists(end_file):
        id = os.path.split(os.path.split(end_file)[0])[1]
        target_ids.append(id)
        cur.execute("INSERT OR IGNORE INTO users (id) VALUES (%s)" % (id))

conn.commit()

for id in target_ids:
    dir4id = os.path.join(DATA_DIR, id)

    files = []
    for file in os.listdir(dir4id):
        if file.endswith(".json"):
            files.append(os.path.join(dir4id, file))

    extract_json_to_db(id, files)
