import markovify
import random
import json

def main():
  return random_real_or_fake()

def generate():
  model_json = open("base_model.json").read()
  model = markovify.Text.from_json(model_json)
  return model.make_sentence(min_words=5,max_words=12)

def get_fake():
  with open("moderated.json", "r") as raw_data:
    data = json.load(raw_data)['list']
  return random.choice(data)
def get_real():
  with open("data.json", "r") as raw_data:
    data = json.load(raw_data)['data']
  return random.choice(data)

def random_real_or_fake():
  is_real = random.choice([True, False])
  if is_real:
    return (get_real(), is_real)
  else:
    return (get_fake(), is_real)