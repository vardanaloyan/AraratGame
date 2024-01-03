from random import randint
import json
N = 30
Max = 30
Min = 0
d = {}
while N >= Min:
    c = randint(Min, Max)
    a = randint(Min, c)
    if a == c:
        continue
    b = c - a
    if f"{c}.png" not in d.values():
        d[f"{a} + {b}"] = f"{c}.png"
    elif f"{a}.png" not in d.values():
        d[f"{c} - {b}"] = f"{a}.png"
    else:
        continue
    N -= 1
    
print(json.dumps(d, indent=4))
print(len(d))