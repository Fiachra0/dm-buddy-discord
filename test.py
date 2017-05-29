import random

def standard_character():
    results = ""
    for x in range(0, 6):
       z = random.sample(range(1,7), 4)
       z.remove(min(z))
       stat = sum(z)
       results += "{}, ".format(stat)
    return results[:-2]

print ("{}".format(standard_character()))
