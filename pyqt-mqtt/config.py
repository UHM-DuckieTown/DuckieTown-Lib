import socket

ip_duck = '';
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
ip_duck = s.getsockname()[0]
duck1_feed1 = ip_duck + "_feed1"
#Secondary Feeds to show Raw, Edges, Line Tracker Image, White, and Yellow Mask
duck1_feed2 = ip_duck + "_feed2"
#Subscribed-Topics
duck1_text = ip_duck + "_text"
duck1_slider = ip_duck + "_slider"
duck1_flag = ip_duck + "_flag"

#def getter():
#    return test
