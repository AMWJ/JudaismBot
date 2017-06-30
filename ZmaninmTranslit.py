#!/usr/bin/env python
# -*- coding: utf-8 -*-

// from ummmbacon

import hdate
import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import praw
import praw.exceptions
from polyglot.transliteration import Transliterator

reddit_app_key = ""
reddit_app_secret = ""
reddit_user_name = ""
reddit_user_password = ""
reddit_user_agent = ""
subreddit_name = "Judaism"

reddit = praw.Reddit(user_agent=reddit_user_agent,
                     client_id=reddit_app_key,
                     client_secret=reddit_app_secret,
                     username=reddit_user_name,
                     password=reddit_user_password)

transliterator = Transliterator(source_lang="he", target_lang="en")
geolocator = Nominatim()
tf = TimezoneFinder()


def is_hebrew(term):
    return any("\u0590" <= c <= "\u05EA" for c in term)


def transliterate(phrase):
    return transliterator.transliterate(phrase)


def get_zmanim(address):
    c = geolocator.geocode(address)
    timezone = tf.timezone_at(lng=c.longitude, lat=c.latitude)

    if timezone is None:
        return "Could not locate address"

    z = hdate.Zmanim(date=datetime.date(2016, 4, 18), latitude=c.latitude, longitude=c.longitude, timezone=timezone,
                     hebrew=False, )

    return c, timezone, z


for comment in reddit.subreddit(subreddit_name).stream.comments():
    if is_hebrew(comment.body):
        print(comment.body)
