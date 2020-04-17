# Cloud-task-fault-tolerant-scheduling
 Implement FESTAL and FASTER scheduling algorithms

**Run**
```
FASTER.py
run this file to show the scheduling results on independent or dependent tasks
```
**You could modify the parameters as follows:**
```
Slecet independent or denpendent tasks:
    FESTAL - dependence = False
    FASTER - dependence = True

Active dynamic resource utilization process:
    Dynamic = True

close dynamic resource utilization:
    Dynamic = False

Number of tasks for scheduling:
    num_task = 500

Initilize the cloud platform resources:
    initial number of hosts and VMs per host:
        num_vm = 2
        num_host = 2
    set the maximum resources that are available:
        max_vm = 10
        max_host = 10
```
**modules**
```
Cloudelets.py
    Randomly generate cloudlets(tasks) list
    You can modify the deadline and task size for generated tasks in this file

Resource.py
    Dynamically change the resource utilization
    
Scheduler.py
    Primary and Backup sheduling 
```
