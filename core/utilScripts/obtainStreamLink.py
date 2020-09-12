import streamlink

def getStreamLink(link, option = None):
    streams = streamlink.streams(link)
    if (option is None):
    	option = list(streams.keys())[0]
    else:
    	assert option in list(streams.keys())
    streamLink = streams[option].url
    return streamLink