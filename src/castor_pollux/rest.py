# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from os import environ
import requests
from .adapter import discern


gemini_key              = environ.get('GOOGLE_API_KEY','') # GEMINI_KEY', '')
gemini_api_base         = environ.get('GEMINI_API_BASE','https://generativelanguage.googleapis.com/v1beta')
gemini_content_model    = environ.get('GEMINI_DEFAULT_CONTENT_MODEL', 'gemini-2.5-pro')
gemini_embedding_model  = environ.get('GEMINI_DEFAULT_EMBEDDING_MODEL', 'text-embedding-004')

garbage = [
    {'category':'HARM_CATEGORY_HATE_SPEECH', 'threshold': 'BLOCK_NONE'},
    {'category':'HARM_CATEGORY_SEXUALLY_EXPLICIT', 'threshold': 'BLOCK_NONE'},
    {'category':'HARM_CATEGORY_DANGEROUS_CONTENT', 'threshold': 'BLOCK_NONE'},
    {'category':'HARM_CATEGORY_HARASSMENT', 'threshold': 'BLOCK_NONE'},
    {'category':'HARM_CATEGORY_CIVIC_INTEGRITY', 'threshold': 'BLOCK_NONE'}
]


def continuation(text=None, contents=None, instruction=None, **kwargs):
    """A continuation of text with a given context and instruction.
        kwargs:
            temperature     = 0 to 1.0
            top_p           = 0.0 to 1.0
            top_k           = The maximum number of tokens to consider when sampling.
            n               = 1 is mandatory for this method continuationS have n > 1
            max_tokens      = number of tokens
            stop            = ['stop']  array of up to 4 sequences
    """
    instruction         = kwargs.get('system_instruction', instruction)
    system_instruction  = dict(role='system', parts=[dict(text=instruction)]) if instruction else None

    contents            = kwargs.get('contents', contents)

    # Create a structure that the idiots want.
    human_says = dict(role='user', parts=[dict(text=text)])
    if text and not contents:
        contents = [human_says]
        # contents = [{'parts': [{'text': text}], 'role': 'user'}]
    else:
        contents.append(human_says)
        # {'parts': [{'text': text}], 'role': 'user'})

    # Trickery for thinking models
    thinking_config = None
    model = kwargs.get("model", gemini_content_model)
    if model.startswith('gemini-2.5'):
        thinking_config = {
            'includeThoughts': kwargs.get('include_thoughts', True),
            'thinkingBudget': kwargs.get('thinking_budget', 0)
        }
    elif model.startswith('gemini-3'):
        thinking_config = {
            'includeThoughts': kwargs.get('include_thoughts', True),
            'thinkingLevel': kwargs.get('thinking_level', 'high')
        }

    json_data = {
        'systemInstruction':        system_instruction,
        'contents':                 contents,
        'tools': [
            # {
            #     "file_search": {"file_search_store_names": ["store_name"]}
            # }
        ],
        'safetySettings':           garbage,
        'generationConfig':{
            'stopSequences':        kwargs.get('stop_sequences', ['STOP','Title']),
            'responseMimeType':     kwargs.get('mime_type','text/plain'),
            # 'responseSchema': {},
            'responseModalities':   kwargs.get('modalities',['TEXT']),
            'temperature':          kwargs.get('temperature', 0.5),
            'maxOutputTokens':      kwargs.get('max_tokens', 10000),
            'candidateCount':       kwargs.get('n', 1),  # is in continuationS
            'topP':                 kwargs.get('top_p', 0.9),
            'topK':                 kwargs.get('top_k', 10),
            'enableEnhancedCivicAnswers':   False,
            #'cachedContent': '',
        },
    }
    if thinking_config:
        json_data['generationConfig']['thinkingConfig'] = thinking_config

    try:
        response = requests.post(
            url=f'{gemini_api_base}/models/{kwargs.get("model", gemini_content_model)}:generateContent',
            params=f'key={gemini_key}',
            json=json_data,
        )
        if response.status_code == requests.codes.ok:
            output = response.json()
            text, thoughts = discern(output)
        else:
            print(f'Request status code: {response.status_code}')
            return '', ''

    except Exception as e:
        print(f'Unable to generate continuation of the text, {e}')
        return '', ''

    return text, thoughts


def embed(input_list, **kwargs):
    """Returns the embedding of a list of text strings.
    """
    embeddings_list = []
    json_data = {'texts': input_list} | kwargs
    try:
        response = requests.post(
            f'{gemini_api_base}/models/{kwargs.get("model", gemini_embedding_model)}:batchEmbedText',
            params=f'key={gemini_key}',
            json=json_data,
        )
        if response.status_code == requests.codes.ok:
            # embeddings_list = response.json()['embeddings']
            for count, candidate in enumerate(response.json()['embeddings']):
                item = {'index': count, 'embedding': candidate['value']}
                embeddings_list.append(item)
        else:
            print(f'Request status code: {response.status_code}')
        return embeddings_list
    except Exception as e:
        print('Unable to generate Embeddings response')
        print(f'Exception: {e}')
        return embeddings_list


def create_file_store(display_name, **kwargs):
    """Returns the file search store dict.
    """
    store = {}
    json_data = {'displayName': display_name} | kwargs
    try:
        response = requests.post(
            f'{gemini_api_base}/fileSearchStores',
            params=f'key={gemini_key}',
            json=json_data,
        )
        if response.status_code == requests.codes.ok:
            store = response.json()
        else:
            print(f'Request status code: {response.status_code}')
        return store
    except Exception as e:
        print('Unable to generate a file store')
        print(f'Exception: {e}')
        return store


if __name__ == '__main__':
    # name = 'Castor Pollux'
    store_name = 'fileSearchStores/castor-pollux-nnfpl9z1b3iw'
    # result = create_file_store(name)['name']


    ...
