USER_AGENT = 'WHOSpeechAnalysis/1.0'
URL_TLD = 'http://who.int'
API_SPEECHES = f'{URL_TLD}/api/hubs/speeches?$orderby=PublicationDateAndTime&$select=Title,ItemDefaultUrl,FormatedDate&$skip={{skip}}'
URL_ROBOTS = f'{URL_TLD}/robots.txt'
URL_SPEECHES = f'{URL_TLD}/director-general/speeches/{{page}}'
WEB_DELAY = 2
