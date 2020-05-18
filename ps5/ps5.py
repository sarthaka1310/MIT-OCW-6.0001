# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Sarthak Agrawal
# Collaborators: -
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
import re

#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):

    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid 
        
    def get_title(self):
        return self.title
        
    def get_description(self):
        return self.description
        
    def get_link(self):
        return self.link
       
    def get_pubdate(self):
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    
    def __init__(self, phrase):
        self.phrase = phrase

    def is_phrase_in(self, check_phrase):
        phrase = self.phrase
        
        # replacing punctuations with spaces
        # alternatively: phrase = ''.join([c if c not in punct for c in phrase])
        for ch in string.punctuation:
            phrase = phrase.replace(ch, ' ')
            check_phrase = check_phrase.replace(ch, ' ')

        #cleaning the multiple spaces
        # faster than both   re.sub(' {2}), ' ', phrase)    and     " ".join(phrase.split())
        while '  ' in phrase:
            phrase = phrase.replace('  ', ' ')
        while '  ' in check_phrase:
            check_phrase = check_phrase.replace('  ', ' ')
        
        """
        this was for when I didnt use regex, but that still would give a wrong answer since there was no word bound
        phrase = phrase.strip(' ')
        check_phrase = check_phrase.strip(' ')
        phrase = phrase.lower()
        check_phrase = check_phrase.lower()
        return check_phrase.find(phrase)
        """
        
        rgx = '\\b' + phrase + '\\b' #the regex expression with word binds on the ends of string to be searched
        return re.search(rgx, check_phrase, flags=re.IGNORECASE)!=None

# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):

    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)

    def evaluate(self, story):
        return (self.is_phrase_in(story.get_title()))

# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)
    
    def evaluate(self, story):
        return (self.is_phrase_in(story.get_description()))

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):

    def __init__(self, est):
        self.est = datetime.strptime(est,'%d %b %Y %H:%M:%S').replace(tzinfo=pytz.timezone('EST'))

# Problem 6
# TODO: BeforeTrigger and AfterTrigger

class BeforeTrigger(TimeTrigger):

    def __init__(self, est):
        TimeTrigger.__init__(self,est)
    
    def evaluate(self, story):
        return story.get_pubdate().replace(tzinfo=pytz.timezone('EST')) < self.est
# why doesnt astimezone() work as a replacement for replace?

class AfterTrigger(TimeTrigger):

    def __init__(self, est):
        TimeTrigger.__init__(self,est)
    
    def evaluate(self, story):
        return story.get_pubdate().replace(tzinfo=pytz.timezone('EST')) > self.est


# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, trig):
        self.trig = trig
    
    def evaluate(self, story):
        return not self.trig.evaluate(story)

# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):

    def __init__(self, trig1, trig2):
        self.trig1 = trig1
        self.trig2 = trig2
    
    def evaluate(self, story):
        return self.trig1.evaluate(story) and self.trig2.evaluate(story)


# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):

    def __init__(self, trig1, trig2):
        self.trig1 = trig1
        self.trig2 = trig2
    
    def evaluate(self, story):
        return self.trig1.evaluate(story) or self.trig2.evaluate(story)

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)

    #list comprehension iterates over the stories with iterator "story" and adds in returned list if it fires any trigger "trig" present in triggerlist
    return [story for story in stories if any(trig.evaluate(story) for trig in triggerlist)]

#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    lines = [i.split(',') for i in lines] # each operation is split into words and stored as a list of strings in its own index

    trig = {} # to allocate trigger objects to t1,t2,...
    trigobs=[] # the final list of trigger objects to be returned

    for i in lines:
        if i[0]=='ADD':
            del i[0] #remove the word "add" and then include everything in our list
            for j in i: 
                trigobs.append(trig[j])
        else:
            if i[1]=='TITLE':
                trig[i[0]] = TitleTrigger(i[2])
            elif i[1]=='DESCRIPTION':
                trig[i[0]] = DescriptionTrigger(i[2])
            elif i[1]=='AFTER':
                trig[i[0]] = AfterTrigger(i[2])
            elif i[1]=='BEFORE':
                trig[i[0]] = BeforeTrigger(i[2])
            elif i[1]=='NOT':
                trig[i[0]] = NotTrigger(trig[i[2]]) 
            elif i[1]=='AND':
                trig[i[0]] = AndTrigger(trig[i[2]], trig[i[3]])
            elif i[1]=='OR':
                trig[i[0]] = OrTrigger(trig[i[2]], trig[i[3]])

    return trigobs

SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        """
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]
        """

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()