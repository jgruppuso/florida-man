import json
from main import generate

moderated_list = set()
def save():
  with open("moderated.json", "w") as good_db:
    lst = list(moderated_list)
    output = {'list': lst}
    json.dump(output, good_db, indent=4)

with open("moderated.json", "r") as good_db:
  moderated_list = set(json.load(good_db)["list"])
while True:
  fake_str = generate()
  print(fake_str)
  usr_input = input("Good? (y/n/q)")
  if usr_input == 'y':
    moderated_list.add(fake_str)
  elif usr_input == "n":
    continue
  elif usr_input == "q":
    save()
    break
  else:
    continue

