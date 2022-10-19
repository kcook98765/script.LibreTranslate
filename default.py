import xbmc, xbmcgui
import sys
import urllib.request
import json

win = xbmcgui.Window(10000)
win.setProperty("libreTranslate_text", '')

def main():
    addon = xbmcaddon.Addon("script.LibreTranslate")
    url = addon.getSetting('LibreTranslate_url')
    target = addon.getSetting('LibreTranslate_target_lang')
    api_key = addon.getSetting('LibreTranslate_api_key')

    values = {'q': sys.argv[1], 'source': 'auto', 'target': target, 'format': 'text', 'api_key': api_key}
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
    except Exception as e:
        translated_text = str(e)

    win.setProperty("libreTranslate_text", translated_text)
    return ''


if __name__ == '__main__':
    main()
