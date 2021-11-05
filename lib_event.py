# -*- coding: utf-8 -*-

# Global Libaries
from enum import auto

subscribers = dict()


def subscribe(event_name: auto, fn):
    if event_name not in subscribers:
        subscribers[event_name] = []
    subscribers[event_name].append(fn)


def post_event(event_name: auto, data):
    if event_name not in subscribers:
        return
    for fn in subscribers[event_name]:
        fn(data)
