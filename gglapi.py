from simplejson import load as loadjson
from urllib import quote as urlencode

googlenewsurl = "https://ajax.googleapis.com/ajax/services/search/news?v=1.0" + \
        "&q=SEARCH&key=ABQIAAAAyABxmfS34tEMlt2UD9HT2hSN4OZNJRcNb-mTkbWyVBE6-ADJ1BSpSdvs_0bBvtx5eI3evqY9t0U4rA&userip=87.113.4.205"

def pressMentions(term):
    enc_term = urlencode('source:"racing post" "' + term + '"')
    request = urlopen(googlenewsurl.replace("SEARCH", enc_term))
    results = loadjson(request)
    try:
        return results["responseData"]['cursor']['estimatedResultCount']
    except: 
        return 0


