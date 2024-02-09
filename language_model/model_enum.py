#file: model_enum.py 

from enum import Enum
from pathlib import Path
from os.path import abspath

# track downloaded models
class Model(Enum):
    MISTRAL = abspath("../models/mistral-7b-instruct-v0.1.Q4_0.gguf").replace('\\','/')
    ORCA = abspath("../models/orca-mini-3b-gguf2-q4_0.gguf").replace('\\','/')


