import matplotlib.pyplot as plt
import json
import numpy as np
import datetime

data = json.load(open('export.json'))

x = [i for i in range(len(data['untouched']))]
y1 = data['dead']
y2 = data['infected']
y3 = data['recovered']
y4 = data['untouched']

y = np.vstack([y1, y2, y3])

labels = ["Dead ", "Infected", "Recovered", "Infectable"]

fig, ax = plt.subplots()
ax.stackplot(x, y1, y2, y3, y4, labels=labels)
ax.legend(loc='upper left')
date = datetime.datetime.now()
plt.savefig(f"Virus plot export {date.day}-{date.month}-{date.year} {date.hour}_{date.minute}.{date.second}.png")
plt.show()