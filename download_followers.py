import random
import time
import insta_crawler
import os
import json
import logging
import sqlite3
import requests
import traceback

DATA_DIR = "./data"
USER_DICT = {}
NEXT_USER_DICT = {}
COMPL_USER_DICT = {}
USER_ID, USER_PASSWORD = "smileman_god@naver.com","zaq12345"

USE_CENTRAL_DB = False
CENTRAL_DB_URL = "http://engear.net/php-crud-api/api.php/insta_ids"

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
                # if USE_CENTRAL_DB == True:
                #     start_time = time.time()
                #
                #     data = {'insta_id':node["node"]["id"], 'username':node['node']['username'], 'updated':0}
                #     requests.post(CENTRAL_DB_URL,data= json.dumps(data))
                #
                #     elapsed_time = time.time() - start_time
                #     logger.debug("INSERT TO CENTRAL DB : %d ms" % elapsed_time)

                count = count + 1

    conn.commit()
    logger.info("%d users were added." % count)



def download_follows_by_id(id, username = None):
    # id 타겟 dir이 없으면 만든다.
    dir4id = DATA_DIR + "/" + id
    if not os.path.isdir(dir4id):
        os.mkdir(dir4id)

    # 디렉토리 내에 'END'라는 파일이 있으면 해당 폴더의 json 파일을 로드하여 정보를 읽고, 완료 리스트에 저장한다.
    if os.path.exists(dir4id+"/END"):
        files = []
        # dir4id 디렉토리 안의 *.json파일 목록을 구한다.
        for file in os.listdir(dir4id):
            if file.endswith(".json"):
                files.append(os.path.join(dir4id, file))
        logger.info("Loading follows for '%s'(%s)." % (username,id))
        load_json_objects(files)
        if username != None :
            COMPL_USER_DICT[id]= username
        else:
            COMPL_USER_DICT[id]= id

        if USE_CENTRAL_DB == True:
            start_time = time.time()

            resp = requests.get(CENTRAL_DB_URL+"?filter=insta_id,eq,"+id)
            json_data =  json.loads( resp.text)
            if len(json_data["insta_ids"]["records"]) >  0:
                cent_id = json_data["insta_ids"]["records"][0][0]
                data_updated = {'updated':1}
                resp = requests.put(CENTRAL_DB_URL+"/"+str(cent_id),data=json.dumps(data_updated))

            else:
                logger.warning("ID "+ id + " is not exists in CENTRAL DB. Will be INSERTED.")
                data = {'insta_id': id, 'updated': 1}
                resp = requests.post(CENTRAL_DB_URL, data=json.dumps(data))
                if resp.status_code != 200:
                    logger.warning("INSERT ERROR ===>" + str(data) )

            elapsed_time = time.time() - start_time
            logger.debug("INSERT TO CENTRAL DB : %d ms" % elapsed_time)

        return

    file_idx = 0

    while True:
        file_idx = file_idx + 1
        file_name = "%08d_follows_%s_%s.json" % (file_idx, id, username)

        try:
            if file_idx == 1:
                json_follows = ic.get_follows_by_id(id)  # "1408289748"
            else :
                json_follows = ic.get_follows_by_id(id, after=after)
        except insta_crawler.CrawlerException as e:
            logger.fatal("Exception from get_follows_by_id ===>")
            logger.fatal( e.getObject())
            file_idx = file_idx -1
            waits = random.randrange(5, 20)
            logger.info("Waiting for %d seconds." % waits)
            time.sleep(waits)
            continue
        except requests.exceptions.ConnectionError as ce:
            logger.fatal("Exception from get_follows_by_id(Connection Error)===>")
            logger.fatal(str(ce))
            file_idx = file_idx -1
            waits = random.randrange(5, 20)
            logger.info("Waiting for %d seconds." % waits)
            time.sleep(waits)
            continue
        except KeyError as ke :
            logger.fatal("Exception from get_follows_by_id(Key Error)===>")
            logger.fatal(str(ke))
            file_idx = file_idx -1
            waits = random.randrange(5, 20)
            logger.info("Waiting for %d seconds." % waits)
            time.sleep(waits)
            ic.init()
            ic.login()
            continue



        if 'status' in json_follows and 'message' in json_follows:
            logger.info("Received wating message.")
            logger.error(json_follows)
            # message:'몇 분 후에 다시 시도해주세요.', status:'fail'
            if json_follows['status'] == 'fail' and json_follows['message'] == '몇 분 후에 다시 시도해주세요.':
                waits = random.randrange(10, 30)
                logger.info("Waiting for %d seconds." % waits)
                time.sleep(waits)
                file_idx = file_idx - 1
                continue

        try:
            for node in  json_follows['data']['user']['edge_follow']['edges']:
                f_id = node['node']['id']
                f_username = node['node']['username']
                if not node["node"]["id"] in COMPL_USER_DICT:
                    NEXT_USER_DICT[f_id] = f_username
        except TypeError as e:
            logger.fatal("NODE ERROR ===>")
            logger.fatal(json_follows)
            waits = random.randrange(10, 20)
            logger.info("Waiting for %d seconds." % waits)
            time.sleep(waits)
            file_idx = file_idx - 1

            #이 에러가 발생하면 계속 데이터를 못 가져오므로 연결 자체를 초기화 해야한다.
            logger.info("Login initialize...")
            ic.init()
            ic.login()
            continue



        outfile_name = dir4id + "/" + file_name
        logger.info("Writing... '%s'" % outfile_name)
        with open(outfile_name, 'w') as outfile:
            json.dump(json_follows, outfile, indent=4)

        if not json_follows['data']['user']['edge_follow']['page_info']['has_next_page'] == True:
            break
        else :
            after = json_follows['data']['user']['edge_follow']['page_info']['end_cursor']

    # 완료가 되면 폴덩 END라는 이름의 파일을 만들고 완료 아이디 리스트에 저장한다.
    touch(dir4id+"/END")
    if username != None :
        COMPL_USER_DICT[id] = username
    else:
        COMPL_USER_DICT[id] = id

    if USE_CENTRAL_DB == True:
        start_time = time.time()

        resp = requests.get(CENTRAL_DB_URL+"?filter=insta_id,eq,"+id)
        json_data =  json.loads( resp.text)
        if len(json_data["insta_ids"]["records"]) > 0:
            cent_id = json_data["insta_ids"]["records"][0][0]
            data_updated = {'updated': 1}
            resp = requests.put(CENTRAL_DB_URL + "/" + str(cent_id), data=json.dumps(data_updated))

        else:
            logger.warning("ID " + id + " is not exists in CENTRAL DB. Will be added.")
            data = {'insta_id': id, 'updated': 1}
            resp = requests.post(CENTRAL_DB_URL, data=json.dumps(data))

        elapsed_time = time.time() - start_time
        logger.debug("INSERT TO CENTRAL DB : %d ms" % elapsed_time)

if __name__ == "__main__":
    logger.info("Start crawling.")



    if os.path.isdir(DATA_DIR) == True :
        logger.info("DATA DIRECTORY '%s' already exists." % DATA_DIR)
    else:
        os.mkdir(DATA_DIR)
        logger.info("DATA DIRECTORY '%s' directory is made." % DATA_DIR)

    ic = insta_crawler.InstaCrawler(USER_ID, USER_PASSWORD)
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
        user_dict_idx = 0
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
            user_dict_idx = user_dict_idx +1
            logger.info("USER_DICT : %d of %d completed." % (user_dict_idx, len(USER_DICT)))
            logger.info("NEXT_USER_DICT : %d" % len(NEXT_USER_DICT))

        break

        logger.info("[%d] iteration completed. Count=%d" % (iter_count,len(USER_DICT)))


        if len(NEXT_USER_DICT) > 0 :
            logger.info("Next User Dict length : %d" % len(NEXT_USER_DICT))
            USER_DICT = NEXT_USER_DICT
            NEXT_USER_DICT = {}

    conn.close()
