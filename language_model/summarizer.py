#file: model.py

from gpt4all import GPT4All

print("Hello!")
model = GPT4All("C:/Users/jackm/Documents/School/Senior/daily-digest/models/orca-mini-3b-gguf2-q4_0.gguf")
output = model.generate("Humans landed on the moon in the year ", max_tokens=10)
print(output)