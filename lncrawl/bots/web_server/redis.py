import redis
import dotenv
import os
from ...models import Chapter
from typing import List
from .constants import get_work_key, get_chapter_key

dotenv.load_dotenv()

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')

DB = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

# given a chapter url, and list of chapters
# set the chapter hash as key and chapter urls hashes as values
# with a lifespan of 1 day
def register_work(url, chapter: List[Chapter]):
    key = get_work_key(url)
    value = [get_chapter_key(c['url']) for c in chapter]
    DB.sadd(key, *value)
    DB.expire(key, 86400)

    for c in chapter:
        key = get_chapter_key(c['url'])
        DB.set(key, c['body'])
        DB.expire(key, 86400)

def get_work(url):
    key = get_work_key(url)
    return DB.smembers(key)