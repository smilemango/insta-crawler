import my_logger
import sqlite3



my_logger.init_mylogger("insta2vec_logger","./log/insta2vec.log")

conn = sqlite3.connect('processce_data/insta_user_relations.sqlite3')
c = conn.cursor()

# SQL 쿼리 실행
c.execute("""
select user_id, follow_id from relations order
""")


