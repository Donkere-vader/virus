import matplotlib.pyplot as plt
import json

data = json.load(open('export.json'))
plt.plot(data['infected'])
plt.plot(data['dead'])

plt.ylabel('Persons')
plt.xlabel("Simulation ticks")

plt.show()