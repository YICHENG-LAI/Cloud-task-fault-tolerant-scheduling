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
num_host = 2
num_vm = 2
max_vm = 10 # max number of VMs in a host
max_host = 10 # max number of hosts in a datacenter
num_task = 100
beta = 0.2 # ratio of cloudlets that have parent cloudlets
tt = 1 # assume transmisson time between cloudlets is 1s

dependence = True # generate dependent cloudlets or not
Dynamic = True # apply dynamic resource utilization or not

# Initialize hosts and VMs
Host = creatDatacenter(num_host,max_vm)
# generate input cloudlets ; t_n = (arrival, deadline, length)
cloudlets = Cloudlets()
tasks = cloudlets.generate_ind(num_task)
Parent = {}
if dependence:
    Parent = cloudlets.generate_d(beta) # parent tasks

print(Parent)

# Scheduling
flag = False # whether all the task have scheduled
# allocation map of tasks to hosts and VMs
allocation = {'host_'+str(i):{'VM_'+str(j):{} for j in range(num_vm)} for i in range(num_host)}
missddl = [] # tasks that will miss the deadline
count = np.zeros([2,num_host]) # count the number of primary allocated tasks and VMs
count[1] = num_vm
task_map = {}

while not flag:
    for i in tasks:
        scheduler = Scheduler(Host, allocation, count, Parent, max_vm, task_map, tt, max_host, Dynamic)
        pr = scheduler.primary(tasks[i], i)  
        bc = scheduler.backup(tasks[i], i)
        Host, allocation, count, task_map = scheduler.get()
        if pr and bc:
            continue
        else:
            missddl.append(i)
        
    # if not missddl:
    #     flag = True
    flag = True
print('---------------------------------------------')
print('Scheduling Finished!')

            ########################
            #      Evalutation     #
            ########################

# Guarantee Ratio
GR = 1 - len(missddl) / num_task
# Host Active Time
all_VM = int(sum(count[1]))
all_host = len(count[0])
vm_active = all_VM * 15
task_time = 0
for i in task_map:
    task_time = max(task_time, task_map[i][1])
HAT = task_time + vm_active
# Ratio of task time over host t
# ime
RTH = task_time / HAT

# print(allocation)
print('---------------------------------------------')
print('Missed Deadline tasks:'+ str(len(missddl)))
print('GR = '+str(GR*100)+'%')
print('HAT = '+str(HAT)+' s')
print('RTH = %-10.2f' %(RTH))
print('Number of VM have been used:'+str(all_VM))
print('Number of Host have been used:'+ str(all_host))