import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import numpy as np

plt.rc('text', usetex=True)
plt.rc('font', family='serif')


sns.set_palette("Paired")
# sns.set_palette("deep")
sns.set_context("poster", font_scale=2)
sns.set_style("whitegrid")
# sns.palplot(sns.color_palette("deep", 10))
# sns.palplot(sns.color_palette("Paired", 9))

color = ['C1', 'C0', 'C3']
label = ['PS-provenance', "PS-searching", "LT"]

f_size = (14, 10)

x_list = list()
x_naive = list()
execution_timeps1 = list()
execution_timeps2 = list()
execution_timelt = list()


input_path = r'constraint_change_q1c2.csv'
input_file = open(input_path, "r")

Lines = input_file.readlines()

count = 0
# Strips the newline character
for line in Lines:
    count += 1
    if line == '\n':
        break
    if count < 2:
        continue
    items = line.strip().split(',')
    x_list.append(items[0])
    execution_timeps1.append(float(items[1]))
    execution_timeps2.append(float(items[2]))
    if len(items) == 4:
        execution_timelt.append(float(items[3]))
    else:
        execution_timelt.append(0)
print(x_list, execution_timeps1, execution_timeps2)

index = np.arange(len(x_list))
bar_width = 0.35

fig, ax = plt.subplots(1, 1, figsize=f_size)


plt.bar(index, execution_timeps1, bar_width, color=color[0], label=label[0])
plt.bar(index, execution_timeps2, bar_width, bottom=execution_timeps1,
        color=color[1], label=label[1])
plt.xticks(index, x_list)

plt.xlabel('White male $\leq$')
plt.ylabel('Running time (s)')
plt.legend(loc='upper right', bbox_to_anchor=(1, 0.73))
# plt.yscale("log")
# plt.yticks([0, 20, 40, 60])
plt.tight_layout()
plt.savefig("adult_constraint_change_q1c2.png",
            bbox_inches='tight')
plt.show()
