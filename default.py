import xbmc, xbmcgui, xbmcaddon
import sys
import urllib.request
import json
import simplecache
import hashlib
import datetime
from urllib.parse import parse_qs
import re

win = xbmcgui.Window(10000)
win.setProperty("libreTranslate_text", '')

_cache = simplecache.SimpleCache()

def main():

    params = {}
    for arg in sys.argv:
        if arg == 'default.py':
            pass
        elif '=' in arg:
            arg_split = arg.split('=', 1)
            if arg_split[0] and arg_split[1]:
                key, value = arg_split
                params.setdefault(key, value)
        else:
            params.setdefault(arg, True)

    q = params.get("q", None)
    p = params.get("property", None)
    
    if q is None:
        q = sys.argv[1]
    
    if p is not None:
        setprop = 'libreTranslate_' + p
    else:
        setprop = 'libreTranslate_text'
    
    win.setProperty(setprop, '')
    
    
    addon = xbmcaddon.Addon("script.LibreTranslate")
    url = addon.getSetting('LibreTranslate_url')
    target = addon.getSetting('LibreTranslate_target_lang')
    api_key = addon.getSetting('LibreTranslate_api_key')
    cache_days = int(addon.getSetting('LibreTranslate_cache_len'))

    if cache_days is None:
        cache_days = 0
    
    md5_result = hashlib.md5(q.encode())
    hash_hex = md5_result.hexdigest()
    
    this_cache_id = 'script.libreTranslate.' + target + '_' + hash_hex

    translated_text = _cache.get(this_cache_id)

    if translated_text:
        _cache.set( this_cache_id, translated_text, expiration=datetime.timedelta(days=cache_days))
        if cache_days > 0:
            win.setProperty(setprop, translated_text)
            return ''

    values = {'q': q, 'source': 'auto', 'target': target, 'format': 'text', 'api_key': api_key}
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }    
    data = json.dumps(values).encode("utf-8")
    
    try:
        req = urllib.request.Request(url, data, headers)
        with urllib.request.urlopen(req) as f:
            res = f.read()
            result = json.loads(res)
            translated_text = str(result['translatedText'])
            translated_text = re.sub(r"^[\ \'\"]+", "", translated_text)
            translated_text = re.sub(r"[\ \"\']+$", "", translated_text)
            translated_text = re.sub(r"\"\.+$", ".", translated_text)
            _cache.set( this_cache_id, translated_text, expiration=datetime.timedelta(days=cache_days))
    except Exception as e:
        translated_text = str(e)

    win.setProperty(setprop, translated_text)
    return ''


if __name__ == '__main__':
    main()
