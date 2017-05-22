import insta_crawler
import pprint
import os
import json

DATA_DIR = "./data"
USER_DICT = []


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
    print("xx")

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

        load_json_objects(files)
        return

    json_follows = ic.get_follows_by_id(id)  # "1408289748"
    # pprint.pprint(json_follows)
    # json_follows['data']['user']['edge_follow']['page_info']['end_cursor']
    # json_follows['data']['user']['edge_follow']['page_info']['has_next_page']
    #
    file_idx = 0

    while json_follows['data']['user']['edge_follow']['page_info']['has_next_page'] == True:
        file_idx = file_idx + 1
        file_name = "%08d_follows_%s_%s.json" % (file_idx, id, username)

        if file_idx > 1:
            json_follows = ic.get_follows_by_id(id, after=json_follows['data']['user']['edge_follow']['page_info'][
                'end_cursor'])

        for node in  json_follows['data']['user']['edge_follow']['edges']:
            f_id = node['node']['id']
            f_username = node['node']['username']
            USER_DICT.append({"id":f_id, "username":f_username})

        outfile_name = dir4id + "/" + file_name
        print("Writing... '%s'" % outfile_name)
        with open(outfile_name, 'w') as outfile:
            json.dump(json_follows, outfile, indent=4)

    touch(dir4id+"/END")


if __name__ == "__main__":
    if os.path.isdir(DATA_DIR) == True :
        print("'%s' directory already exists." % DATA_DIR)
    else:
        os.mkdir(DATA_DIR)
        print("'%s' directory is made." % DATA_DIR)

    ic = insta_crawler.InstaCrawler("smileman_god@naver.com","my password")
    ic.login()
    print(ic.is_logged_in())

    download_follows_by_username("lovelymrsyi")
    input("Press any key...")


    for user in USER_DICT:
        print("Downloading... '%s'" % user['username'])
        download_follows_by_id(user["id"], username=user['username'])
        print("[OK]")
        input("Press any key...")
