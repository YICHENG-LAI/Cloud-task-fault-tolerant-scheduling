import numpy as np

class Resource():
    def __init__(self, max_vm):
        self.max_vm = max_vm
        self.host_id = 0 
        self.vm_name = '' 

    def scale_up(self, allocation_map, count):
        host_idx = np.argsort(count[1])
        for i in host_idx:
            host_name = 'host_'+ str(i)
            num_vm = len(allocation_map[host_name])
            if num_vm < self.max_vm:
                vm_id = num_vm
                self.vm_name = 'VM_' + str(vm_id)
                self.host_id = i
                print('Adding a new VM to '+'host_'+str(i)+'...')
                return True
            else:
                continue
        return False


    def get(self):
        return self.host_id, self.vm_name