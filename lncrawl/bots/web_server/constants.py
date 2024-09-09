import hashlib


"""
 # redis db struc 
    - works
        - key - url hash
        - value - keys to chapters
    - chapters
        - key - url hash
        - value - chapter
"""

def hash_url(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()

CHAPTER_STORE = 'chapters/'
WORK_STORE = 'works/'

def get_work_key(url: str) -> str:
    return WORK_STORE + hash_url(url)

def get_chapter_key(url: str) -> str:
    return CHAPTER_STORE + hash_url(url)