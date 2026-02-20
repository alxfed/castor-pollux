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
        if part.get('thoughts'):
            thoughts += part['text']
        else:
            text += part['text']

    return text, thoughts
