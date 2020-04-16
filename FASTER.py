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
num_task = 50
beta = 0.2 # ratio of cloudlets that have parent cloudlets
dependence = True # generate dependent cloudlets or not
tt = 1 # assume transmisson time between cloudlets is 1s


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
        scheduler = Scheduler(Host, allocation, count, Parent, max_vm, task_map, tt)
        pr = scheduler.primary(tasks[i], i)  
        bc = scheduler.backup(tasks[i], i)
        if pr and bc:
            continue
        else:
            missddl.append(i)
        Host, allocation, count, task_map = scheduler.get()
    # if not missddl:
    #     flag = True
    flag = True
print('---------------------------------------------')
print('Scheduling Finished!')
# Guarantee Ratio
GR = 1 - len(missddl) / num_task

# print(allocation)
print('---------------------------------------------')
print('Missed Deadline tasks:'+ str(len(missddl)))
print('GR='+str(GR*100)+'%')