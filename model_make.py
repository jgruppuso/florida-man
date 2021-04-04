import json
import markovify

data = []
with open("data.json", "r") as raw_data:
  data = json.load(raw_data)['data']

print("Done loading")

combined_model = None
for title in data:
  model = markovify.Text(title, retain_original=False, well_formed=False)
  if combined_model:
      combined_model = markovify.combine(models=[combined_model, model])
  else:
      combined_model = model

# Print five randomly-generated sentences
for i in range(5):
    print(combined_model.make_sentence())