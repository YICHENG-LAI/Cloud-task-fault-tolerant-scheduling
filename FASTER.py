from Cloudlets import *
from Scheduler import *

def creatDatacenter(num_host, num_vm):
    host_all = []
    for i in range(num_host):
        h = creatHost(num_vm)
        host_all.append(h)
    return host_all


def creatHost(num_vm):
    host = [[] for _ in range(num_vm)]
    return host

# Initial Parameters
num_host = 4
num_vm = 2
max_vm = 10 # max number of VMs in a host
num_task = 500

# Initialize hosts and VMs
Host = creatDatacenter(num_host,max_vm)
# generate input cloudlets ; t_n = (arrival, deadline, length)
cloudlets = Cloudlets()
tasks = cloudlets.generate_ind(num_task)
# tasks = {'t0': (2, 1402, 100000.0), 't1': (3, 2203, 200000.0), 't2': (8, 9508, 500000.0), 't3': (18, 1118, 100000.0), 't4': (23, 3623, 300000.0), 't5': (26, 3626, 200000.0), 't6': (30, 3030, 200000.0), 't7': (32, 5132, 300000.0), 't8': (37, 7637, 400000.0), 't9': (39, 3639, 200000.0), 't10': 
# (49, 1149, 100000.0), 't11': (59, 5759, 300000.0), 't12': (69, 4569, 300000.0), 't13': (74, 4274, 300000.0), 't14': (84, 7084, 500000.0), 't15': (94, 2694, 200000.0), 't16': (99, 1799, 100000.0), 't17': (103, 5503, 300000.0), 't18': (109, 1909, 100000.0), 't19': (116, 4916, 300000.0), 't20': (118, 1918, 100000.0), 't21': (119, 1419, 100000.0), 't22': (122, 4022, 300000.0), 't23': (123, 5523, 300000.0), 't24': (128, 5528, 300000.0), 't25': (136, 6636, 500000.0), 't26': (144, 1444, 100000.0), 't27': (148, 3948, 200000.0), 't28': (149, 4649, 300000.0), 't29': (151, 1651, 100000.0), 't30': (156, 7356, 400000.0), 't31': (159, 2759, 200000.0), 't32': (159, 7659, 
# 500000.0), 't33': (162, 4662, 300000.0), 't34': (170, 1770, 100000.0), 't35': (179, 10179, 500000.0), 't36': (182, 1382, 100000.0), 't37': (186, 5686, 500000.0), 't38': (196, 3196, 200000.0), 't39': (200, 1600, 100000.0)}
Parent = [] # parent tasks
print(tasks)

# Scheduling
flag = False # whether all the task have scheduled
# allocation map of tasks to hosts and VMs
allocation = {'host_'+str(i):{'VM_'+str(j):{} for j in range(num_vm)} for i in range(num_host)}
missddl = [] # tasks that will miss the deadline
count = np.zeros([2,num_host]) # count the number of primary allocated tasks and VMs
count[1] = num_vm

while not flag:
    for i in tasks:
        scheduler = Scheduler(Host, allocation, count, Parent, max_vm)
        pr = scheduler.primary(tasks[i], i)  
        bc = scheduler.backup(tasks[i], i)
        if pr and bc:
            continue
        else:
            missddl.append(i)
        Host, allocation, count = scheduler.get()
    # if not missddl:
    #     flag = True
    flag = True

# Guarantee Ratio
GR = 1 - len(missddl) / num_task

# print(allocation)
print(missddl)
print('GR='+str(GR*100)+'%')