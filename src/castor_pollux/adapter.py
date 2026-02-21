# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""


def discern(output):
    text = ''
    thoughts = ''
    if output['candidates'][0]['finishReason'] == 'SAFETY':
        raise Exception('Answer censored by Google.')
    for part in output['candidates'][0]['content']['parts']:
        if part.get('thought'):
            thoughts += part['text']
        else:
            text += part['text']

    return text, thoughts


def messages_to_mpj(messages):
    contents = []
    for message in messages:
        if message['role'] == 'user':
            obj = dict(role='user', parts=[dict(text=message['content'])])
        elif message['role'] == 'assistant':
            obj = dict(role='model', parts=[dict(text=message['content'])])
        else:
            obj = {}
        contents.append(obj)
    return contents