from botocore.vendored import requests
import datetime

def mnth(var):
    mnths = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    idx = int(var)
    return mnths[idx]

def lambda_handler(event, context):
    r = requests.get('http://codeforces.com/api/contest.list')
    r = r.json()
    final_return = ''
    
    if r["status"] != "OK":
        final_return = 'Oops, A network error'
    else:
        resultsArray = r["result"]
        UpcomingContests = []
        startTimeSeconds = -1
    
        for eachArray in resultsArray:
            if eachArray["phase"] == "BEFORE":
                UpcomingContests.append(eachArray)
                if startTimeSeconds == -1:
                    startTimeSeconds = eachArray["startTimeSeconds"]
                if eachArray["startTimeSeconds"] < startTimeSeconds:
                    startTimeSeconds = eachArray["startTimeSeconds"]
    
        if len(UpcomingContests) == 0:
            final_return = 'Seems like a bad day. there are no upcoming contests.'
            
        for eachArray in UpcomingContests:
            if startTimeSeconds == eachArray["startTimeSeconds"]:
                minutes = startTimeSeconds / 60
                hours = minutes / 60
                minutes = minutes - (hours * 60)
                seconds = startTimeSeconds % 60
    
                Day = datetime.datetime.fromtimestamp(int(startTimeSeconds)).strftime("%d ")
                Month = datetime.datetime.fromtimestamp(int(startTimeSeconds)).strftime("%m")
                mid = mnth(Month)
                Rem = datetime.datetime.fromtimestamp(int(startTimeSeconds)).strftime(" %Y at %H hours %M minutes ")
    
                speakText = "The next contest is " + str(eachArray["name"]) + " It starts on "
                speakText = speakText + Day + mid + Rem
                speakText = speakText + ". I wish you high rating. Good luck and have fun."
                final_return = str(speakText)
        
    response = {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': str(final_return),
            }
        }
    }
    return response
