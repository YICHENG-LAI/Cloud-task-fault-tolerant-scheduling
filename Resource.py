import numpy as np

class Resource():
    def __init__(self, max_vm, max_host):
        self.max_vm = max_vm
        self.max_host = max_host
        self.host_id = 0 
        self.vm_name = '' 
        self.count = []

    def scale_up(self, allocation_map, count):
        self.count = count
        host_idx = np.argsort(count[1])
        # try to activate new VM
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
        print('Add new VM failed... ')
        print('Try to activate a new host...')
        # try to activate a new host
        num_host = len(self.count[0])
        if num_host < self.max_host:
            tmp_count = np.zeros([2,num_host+1])
            tmp_count[:,:-1] = count
            self.count = tmp_count
            self.host_id = num_host
            self.vm_name = 'VM_' + str(0)
            return True
        print('Activate host failed...')
        return False


    def get(self):
        return self.host_id, self.vm_name, self.count