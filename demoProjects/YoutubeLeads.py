from googleapiclient.discovery import build
from pprint import pprint

api_key = 'AIzaSyBVZH_PUswG_ebDrkt01WPthLnf1s7hQYU'





def get_search_results(youtube, query, maxresults=50):

    nextPageToken = None
    noOfResults = 50
    while noOfResults > 0:
        new_response = youtube.search().list(part='snippet', type='video', q=query, maxResults=maxresults, pageToken=nextPageToken).execute()
        noOfResults = new_response['pageInfo']['resultsPerPage']
        if new_response['nextPageToken']:
            yield new_response
            nextPageToken = new_response['nextPageToken']
        else:
            break


youtube = build('youtube', 'v3', developerKey=api_key)
q = 'make money online'
search = get_search_results(youtube, q)
for i in search:
    print(i)
