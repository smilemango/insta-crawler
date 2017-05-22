import random
import time
import insta_crawler
import os
import json
import logging
import sqlite3

DATA_DIR = "./data"
USER_DICT = {}
NEXT_USER_DICT = {}
COMPL_USER_DICT = {}

logger = logging.getLogger("main_logger")

formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

fileHandler = logging.FileHandler('./log/download_followers.log')
fileHandler.setFormatter(formatter)
streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)


logger.addHandler(fileHandler)
logger.addHandler(streamHandler)

fileHandler.setLevel(logging.DEBUG)
streamHandler.setLevel(logging.INFO)

logger.setLevel(logging.DEBUG)

conn = sqlite3.connect("./data/insta-users.sqlite3")




def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


def download_follows_by_username(username):
    if ic.is_logged_in() == True:
        id = ic.get_id_by_username(username)
        download_follows_by_id(id,username)
        return True
    else :
        return False

def load_json_objects(files):
    logger.info("load json files --> %s" % files)
    count = 0

    cur = conn.cursor()
    for file in files:
        with open(file) as data_file:
            data = json.load(data_file)
            for node in data["data"]["user"]["edge_follow"]["edges"]:
                if not node["node"]["id"] in COMPL_USER_DICT:
                    NEXT_USER_DICT[node["node"]["id"]]= node["node"]["username"]
                cur.execute("INSERT OR IGNORE INTO users (id, username) VALUES (%s, '%s')" % (node["node"]["id"], node["node"]["username"]))
                count = count + 1

    conn.commit()
    logger.info("%d users were added." % count)



def download_follows_by_id(id, username = None):
    # id 타겟 dir이 없으면 만든다.
    dir4id = DATA_DIR + "/" + id
    if not os.path.isdir(dir4id):
        os.mkdir(dir4id)

    # 디렉토리 내에 'END'라는 파일이 있으면 패스함
    if os.path.exists(dir4id+"/END"):
        files = []
        for file in os.listdir(dir4id):
            if file.endswith(".json"):
                files.append(os.path.join(dir4id, file))
        logger.info("Loading follows for '%s'(%s)." % (username,id))
        load_json_objects(files)
        if username != None :
            COMPL_USER_DICT[id]= username
        else:
            COMPL_USER_DICT[id]= id

        return

    file_idx = 0

    while True:
        file_idx = file_idx + 1
        file_name = "%08d_follows_%s_%s.json" % (file_idx, id, username)

        if file_idx == 1:
            json_follows = ic.get_follows_by_id(id)  # "1408289748"
        else :
            json_follows = ic.get_follows_by_id(id, after=after)

        if 'status' in json_follows and 'message' in json_follows:
            logger.info("Received wating message.")
            logger.error(json_follows)
            # message:'몇 분 후에 다시 시도해주세요.', status:'fail'
            if json_follows['status'] == 'fail' and json_follows['message'] == '몇 분 후에 다시 시도해주세요.':
                waits = random.randrange(20, 60)
                logger.info("Waiting for %d seconds." % waits)
                time.sleep(waits)
                file_idx = file_idx - 1
                continue

        for node in  json_follows['data']['user']['edge_follow']['edges']:
            f_id = node['node']['id']
            f_username = node['node']['username']
            if not node["node"]["id"] in COMPL_USER_DICT:
                NEXT_USER_DICT[f_id] = f_username

        outfile_name = dir4id + "/" + file_name
        logger.info("Writing... '%s'" % outfile_name)
        with open(outfile_name, 'w') as outfile:
            json.dump(json_follows, outfile, indent=4)

        if not json_follows['data']['user']['edge_follow']['page_info']['has_next_page'] == True:
            break
        else :
            after = json_follows['data']['user']['edge_follow']['page_info']['end_cursor']

    touch(dir4id+"/END")
    if username != None :
        COMPL_USER_DICT[id] = username
    else:
        COMPL_USER_DICT[id] = id


if __name__ == "__main__":
    logger.info("Start crawling.")



    if os.path.isdir(DATA_DIR) == True :
        logger.info("DATA DIRECTORY '%s' already exists." % DATA_DIR)
    else:
        os.mkdir(DATA_DIR)
        logger.info("DATA DIRECTORY '%s' directory is made." % DATA_DIR)

    ic = insta_crawler.InstaCrawler("smileman_god@naver.com","zaq12345")
    ic.login()
    if ic.is_logged_in()== False:
        logger.error("Login failure.")
        exit(-1)

    download_follows_by_username("lovelymrsyi")
    #input("Press any key...")
    iter_count = 1
    USER_DICT= NEXT_USER_DICT
    NEXT_USER_DICT={}
    while len(USER_DICT) != 0 or len(NEXT_USER_DICT) != 0:
        for id in USER_DICT:
            logger.info("Downloading... '%s'" % USER_DICT[id])
            if id in COMPL_USER_DICT:
                logger.info("'%s' is already done. SKIP." % USER_DICT[id])
                continue
            download_follows_by_id(id, username=USER_DICT[id])
            logger.info("[OK]")
            #waits = random.randrange(1,5)
            #logger.info("Waiting %d seconds." % waits)
            #time.sleep(waits)
            #input("Press any key...")

        logger.info("[%d] iteration completed. Count=%d" % (iter_count,len(USER_DICT)))
        if len(NEXT_USER_DICT) > 0 :
            logger.info("Next User Dict length : %d" % len(NEXT_USER_DICT))
            USER_DICT = NEXT_USER_DICT
            NEXT_USER_DICT = {}

    conn.close()
