import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import numpy as np


sns.set_palette("Paired")
# sns.set_palette("deep")
sns.set_context("poster", font_scale=2)
sns.set_style("whitegrid")
plt.rcParams['xtick.major.size'] = 20
plt.rcParams['xtick.major.width'] = 4
plt.rcParams['xtick.bottom'] = True
plt.rcParams['ytick.left'] = True

plt.rc('text', usetex=True)
plt.rc('font', size=70, weight='bold')

color = ['C1', 'C0', 'C7', 'C6']
label = ['PS-prov', "PS-search", "PS-prov\_no\_opt", "PS-search\_no\_opt"]

f_size = (24, 13)

x_list = list()
x_naive = list()
execution_timeps1 = list()
execution_timeps2 = list()
execution_timebl1 = list()
execution_timebl2 = list()


input_path = r'time_4q.csv'
input_file = open(input_path, "r")

Lines = input_file.readlines()

count = 0
# Strips the newline character
for line in Lines:
    count += 1
    if line == '\n':
        continue
    if count < 2:
        continue
    if count > 10:
        break
    items = line.strip().split(',')
    x_list.append(items[0])
    execution_timeps1.append(float(items[1]))
    execution_timebl1.append(float(items[2]))
    # if items[4] != '':
    #     execution_timebl1.append(float(items[5]))
    #     execution_timebl2.append(float(items[6]))
    # else:
    #     execution_timebl1.append(0)
    #     execution_timebl2.append(0)



index = np.arange(len(x_list))
bar_width = 0.45

fig, ax = plt.subplots(1, 1, figsize=f_size)

plt.bar(index, execution_timeps1, bar_width, color=color[1], label=label[1])
# plt.bar(index, execution_timeps2, bar_width, bottom=execution_timeps1,
#         color=color[1], label=label[1])
plt.bar(index + bar_width, execution_timebl1, bar_width, color=color[3], label=label[3])
# plt.bar(index + bar_width, execution_timebl2, bar_width, bottom=execution_timebl1,
#         color=color[3], label=label[3])

# x_list = ['\\boldmath$Q^A_1$\n\\boldmath$C^A_1$', '\\boldmath$Q^A_1$\n\\boldmath$C^A_2$',
#           '\\boldmath$Q^A_2$\n\\boldmath$C^A_1$', '\\boldmath$Q^A_2$\n\\boldmath$C^A_2$']
x_list = ['\\boldmath$Q^A_1$\n\\boldmath$C^A_1$', '\\boldmath$Q^A_1$\n\\boldmath$C^A_2$',
          '\\boldmath$Q^A_2$\n\\boldmath$C^A_1$', '\\boldmath$Q^A_2$\n\\boldmath$C^A_2$',
          '\\boldmath$Q^A_3$\n\\boldmath$C^A_4$', '\\boldmath$Q^A_3$\n\\boldmath$C^A_5$',
          '\\boldmath$Q^A_4$\n\\boldmath$C^A_7$', '\\boldmath$Q^A_4$\n\\boldmath$C^A_8$',
          ]


plt.xticks(np.arange(0, 8) + bar_width/2, x_list, rotation=0, fontsize=80)
plt.yticks(fontsize=80, weight='bold')
plt.ylim(0.01, 10)
plt.xlabel('Query and Constraint', fontsize=85, weight='bold')

plt.yscale('log')
# lgnd = plt.legend(loc='upper left', bbox_to_anchor=(0, 1.2), fontsize=80, ncol=2, labelspacing=0.4,
#                   handletextpad=0.1, markerscale=0.5, columnspacing=0.5)

lgnd = plt.legend(loc='upper left', bbox_to_anchor=(0, 1.2), fontsize=80, ncol=1,
                  labelspacing=0.15, handletextpad=0.1, markerscale=0.5, columnspacing=0.5)


plt.tight_layout()
plt.savefig("ACSIncome_optimization_effect_4q.png", bbox_inches='tight')
plt.show()