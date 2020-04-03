import json

with open("history.json", "r") as f:
  history = json.load(f)

seperations = []
found = False

for k, v in history.items():
  if not found and len(v) > 1:
    found = not found
    print(k, " ", end="")

  if found and len(v) == 1:
    found = not found
    print(str(int(k)-1))

print("---")

apple = ["#8e302e", "#9b322f"]
vals = []
for k, v in history.items():
  found = False
  for vv in v:
    if vv in apple:
      found = True

  if found:
    vals.append(int(k))


for i in range(1, len(vals)):
  if (vals[i] - vals[i-1]) > 1:
    print(vals[i-1], vals[i])


# for i in range(1, len(a)):
#   if a[i]-1 != a[i-1]:
#     print(a[i], a[i-1])
