# castor-pollux
Castor-Pollux (the twin sons of Zeus, routinely called 'gemini') is a pure REST API library for interacting with Google Generative AI API.

## Without (!!!):
- any whiff of 'Vertex' or GCP;
- any signs of 'Pydantic' or unnecessary (and mostly useless) typing;
- any other dependencies of other google packages trashed into the dumpster `google-genai` package.

## Installation:
<pre>
  pip install castor-pollux
</pre>
Then:
```Python
  # Python
  import castor_pollux.rest as cp
```
## A text continuation request:
```Python
import castor_pollux.rest as cp
from yaml import safe_load as yl
from yaml import safe_dump as yd
from yaml import YAMLError as ERR

kwargs = """  # this is a string in YAML format
  model:        gemini-2.5-pro-exp-03-25    # thingking model
  # system_instruction: ''                  # will prevail if put here
  mime_type:    text/plain                  #
  modalities:
    - TEXT                                  # text for text
  max_tokens:   10000
  n:            2                           # 1 is not mandatory
  stop_sequences:
    - STOP
    - "\nTitle"
  temperature:  0.5                         # 0 to 1.0
  top_k:        10                          # number of tokens to consider.
  top_p:        0.5                         # 0 to 1.0
  thinking:     24576                       # thinking tokens budget.
"""

instruction = 'You are Joseph Jacobs, you retell folk tales.'

text_to_continue = 'Once upon a time, when pigs drank wine '

machine_responses = cp.continuation(
    text=text_to_continue,
    instruction=instruction,
    **yl(kwargs)
)

file_name = 'yaml_test.yaml'
with open(file_name, "w") as stream:
    try:
        yd(machine_responses, stream)
    except ERR as exc:
        print(exc)
# texts = yd(machine_responses)
with open(file_name, 'r') as stream:
    try:
        texts = yl(stream)
    except ERR as exc:
        print(exc)
```
## A multi-turn conversation continuation request:
```Python
import castor_pollux.rest as cp
from yaml import safe_load as yl
from yaml import safe_dump as yd
from yaml import YAMLError as ERR

kwargs = """  # this is a string in YAML format
  model:        gemini-2.5-pro-exp-03-25
  system:       Always answer concisely 
  max_tokens:   5
  stop_sequences:   
    - stop          
    - "\n\n\nHuman:"    
  stream:       False 
"""

previous_turns = """
  - role:   human  # not the idiotic 'user', God forbid.
    text: Can we change human nature?
    
  - role:   machine # not the idiotic 'model'
    text: Of course, nothing can be simpler. You just re-educate them.
"""

human_response_to_the_previous_turn = 'That is not true. Think again.'

instruction = 'I am an expert in critical thinking. I analyse.'

machine_responses = cp.continuation(
    text=human_response_to_the_previous_turn,
    contents=yl(previous_turns),
    instruction=instruction,
    **yl(kwargs)
)

file_name = 'yaml_test.yaml'
with open(file_name, "w") as stream:
    try:
        yd(machine_responses, stream)
    except ERR as exc:
        print(exc)
# texts = yd(machine_responses)
with open(file_name, 'r') as stream:
    try:
        texts = yl(stream)
    except ERR as exc:
        print(exc)
``` 