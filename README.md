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

kwargs = """  # this is a string in YAML format
  model:        gemini-3.1-pro-preview      # thingking model
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
  include_thoughts: True
  thinking_level: high                      # for 3+ models
"""

instruction = 'You are Joseph Jacobs, you retell folk tales.'

message = [{"role": "user", "content": 'Once upon a time, when pigs drank wine '}]

machine_responses = cp.continuation(
    messages=message,
    instructions=instruction,
    **yl(kwargs)
)
```
## A continuation with sources:

```Python
import castor_pollux.rest as cp
from yaml import safe_load as yl

kwargs = """  # this is a string in YAML format
  model:        gemini-2.5-pro
  mime_type:    text/plain
  modalities:
    - TEXT
  max_tokens:   32000
  n:            1  # no longer a mandatory 1
  stop_sequences:
    - STOP
    - "\nTitle"
  temperature:  0.5
  top_k:        10
  top_p:        0.5
  include_thoughts: True
  thinking_budget: 32768
  sources:
    - https://github.com/machina-ratiocinatrix
    - https://github.com/alxfed
"""

previous_turns = """
  - role: user
    content: Can we change human nature?
    
  - role: model
    content: Of course, nothing can be simpler. You just re-educate them.
"""

human_response_to_the_previous_turn = 'That is not true. Think again.'

instruction = 'I am an expert in critical thinking. I analyse.'

machine_responses = cp.continuation(
    messages=yl(previous_turns),
    instructions=instruction,
    **yl(kwargs)
)
``` 
