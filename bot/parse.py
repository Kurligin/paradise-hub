import json
from typing import List, Tuple, Optional
import dpath.util
import requests
import re


PATTERNS = [
    re.compile(r'window\["ytInitialData"\] = (\{.+?\});'),
    re.compile(r'var ytInitialData = (\{.+?\});'),
]

session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'


def initialization(url: str) -> Optional[dict]:
    rs = session.get(url)
    
    for pattern in PATTERNS:
        m = pattern.search(rs.text)
        if m:
            data_str = m.group(1)
            return json.loads(data_str)


def video_search(text_or_url: str) -> List[Tuple[str, str]]:
    if text_or_url.startswith('http'):
        url = text_or_url
    else:
        text = text_or_url
        url = f'https://www.youtube.com/results?search_query={text}&sp=EgIQAQ%253D%253D'
    
    items = []
    
    data = initialization(url)
    if not data:
        return items
    
    videos = dpath.util.values(data, '**/videoRenderer')
    if not videos:
        videos = dpath.util.values(data, '**/playlistVideoRenderer')
    
    for video in videos:
        if 'videoId' not in video:
            continue
        
        url = 'https://www.youtube.com/watch?v=' + video['videoId']
        try:
            title = dpath.util.get(video, 'title/runs/0/text')
        except KeyError:
            title = dpath.util.get(video, 'title/simpleText')
        
        items.append((url, title))
    
    return items


