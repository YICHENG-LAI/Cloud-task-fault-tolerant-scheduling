import numpy as np
from Resource import *

class Scheduler():
    def __init__(self, host, allocation_map, count, Parent, max_vm):
        self.Ha = host
        self.map = allocation_map
        self.count = count
        self.r_vm = 15 # assume active a VM need 15s
        self.P = Parent
        self.tt = 0 # assume transmisson time is 0s
        self.VM = 1000 # MIPS
        self.resource = Resource(max_vm)

    def primary(self, task, index):
        # sort hosts by the count of scheduled primary copies
        host_idx = np.argsort(self.count[0])
        alpha = 0
        alpha_end = int(0.5 * len(self.Ha)) # top α% hosts in Ha
        H_candidate = host_idx[alpha:alpha_end] 
        arrival, ddl, length = task
        # init
        eft = float('inf')
        v = None

        # scheduling
        while alpha_end < len(self.Ha):
            for host_id in H_candidate:
                # judgement ......
                # ...
                host_name = 'host_' + str(host_id)
                num_vm = len(self.map[host_name])
                for vm_id in range(num_vm):
                    # earliest start time
                    if not self.P:
                        est_p = max(arrival, self.r_vm)
                    else:
                        f_p = self.P # finish time for parent tasks
                        est_p = max(f_p + self.tt)
                    vm_name = 'VM_' + str(vm_id)
                    if host_name in self.map:
                        if vm_name in self.map[host_name]:
                            for i in self.map[host_name][vm_name]:
                                est_p = max(est_p,self.map[host_name][vm_name][i][1])
                    # runtime for task
                    e_p = length / self.VM
                    # earliest finish time
                    eft_p = est_p + e_p
                    # update eft and VM
                    if eft_p < eft:
                        est = est_p
                        eft = eft_p
                        v = (host_id,vm_id)
            if eft > ddl:
                alpha = alpha_end
                alpha_end += alpha_end 
                H_candidate = host_idx[alpha:alpha_end] 
            else:
                break
        if eft > ddl:
            print('Can not achieve deadline, Allocate task '+index+' Failed')
            print('Try to scale up resources...')
            if self.resource.scale_up(self.map, self.count):
                # allocate task to new VM
                host_id, vm_name = self.resource.get()
                self.count[0][host_id] += 1
                self.count[1][host_id] += 1
                if not self.P:
                        est = max(arrival, self.r_vm)
                else:
                    f_p = self.P # finish time for parent tasks
                    # sj_p strong
                    est = max(f_p + self.tt)
                e_p = length / self.VM
                # earliest finish time
                eft_p = est + e_p
                host_name = 'host_'+ str(host_id)
                T_name = index + '_P'
                T_para = (est,eft_p)
                self.add_map(host_name, vm_name, T_para, T_name)
                print ('Allocate task '+T_name+' to '+host_name+' and '+vm_name+' Success')
                return True
                
                return True
            else:
                # allocation
                # self.count[v[0]][v[1]] += 1
                host_name = 'host_' + str(v[0])
                vm_name = 'VM_' + str(v[1])
                T_name = index + '_P'
                # self.map[host_name] = {vm_name:index}
                print ('Allocate task '+T_name+' to '+host_name+' and '+vm_name+' Failed')
                return False
        else:
                # allocation
                self.count[0][v[0]] += 1
                host_name = 'host_' + str(v[0])
                vm_name = 'VM_' + str(v[1])
                T_name = index + '_P'
                T_para = (est,eft)
                self.add_map(host_name, vm_name, T_para, T_name)
                # self.map[host_name] = {vm_name:{T_name:T_para}}
        print ('Allocate task '+T_name+' to '+host_name+' and '+vm_name+' Success')
        return True
    
    
    def backup(self, task, index):
        # sort hosts by the count of scheduled primary copies
        host_idx = np.argsort(self.count[0])
        alpha = 0
        alpha_end = int(0.5 * len(self.Ha)) # top α% hosts in Ha
        H_candidate = host_idx[alpha:alpha_end] 
        arrival, ddl, length = task
        # init
        eft = float('inf')
        v = None

        # scheduling
        while alpha_end < len(self.Ha):
            for host_id in H_candidate:
                # judgement ......
                # ...
                host_name = 'host_' + str(host_id)
                num_vm = len(self.map[host_name])
                for vm_id in range(num_vm):
                    # earliest start time
                    if not self.P:
                        est_b = max(arrival, self.r_vm)
                    else:
                        f_p = self.P # finish time for parent tasks
                        # sj_p strong
                        est_b = max(f_p + self.tt)
                    vm_name = 'VM_' + str(vm_id)
                    if host_name in self.map:
                        if vm_name in self.map[host_name]:
                            for i in self.map[host_name][vm_name]:
                                est_b = max(est_b,self.map[host_name][vm_name][i][1])
                    # runtime for task
                    e_p = length / self.VM
                    # earliest finish time
                    eft_p = est_b + e_p
                    # update eft and VM
                    if eft_p < eft:
                        est = est_b
                        eft = eft_p
                        v = (host_id,vm_id)  
            if eft > ddl:
                alpha = alpha_end
                alpha_end += alpha_end 
                H_candidate = host_idx[alpha:alpha_end] 
            else:
                break   
        if eft > ddl:
            print('Can not achieve deadline, Allocate task '+index+' Failed')
            print('Try to scale up resources...')
            # scale up the resources
            if self.resource.scale_up(self.map, self.count):
                # allocate task to new VM
                host_id, vm_name = self.resource.get()
                self.count[1][host_id] += 1
                if not self.P:
                    est = max(arrival, self.r_vm)
                else:
                    f_p = self.P # finish time for parent tasks
                    # sj_p strong
                    est = max(f_p + self.tt)
                e_b = length / self.VM
                # earliest finish time
                eft_b = est + e_b
                T_name = index + '_B'
                T_para = (est,eft_b)
                self.add_map(host_name, vm_name, T_para, T_name)
                print ('Allocate task '+T_name+' to '+host_name+' and '+vm_name+' Success')
                return True
            else:
                # allocation
                # self.count[v[0]][v[1]] += 1
                host_name = 'host_' + str(v[0])
                vm_name = 'VM_' + str(v[1])
                T_name = index + '_B'
                # self.map[host_name] = {vm_name:index}
                print ('Allocate task '+T_name+' to '+host_name+' and '+vm_name+' Failed')
                return False
        else:
                # allocation
                host_name = 'host_' + str(v[0])
                vm_name = 'VM_' + str(v[1])
                T_name = index + '_B'
                T_para = (est,eft)
                self.add_map(host_name, vm_name, T_para, T_name)
        print ('Allocate task '+T_name+' to '+host_name+' and '+vm_name+' Success')
        return True


    def get(self):
        return self.Ha, self.map, self.count

    def add_map(self, host_name, vm_name, T_para, T_name):
        if host_name in self.map:
            x = self.map[host_name]
            if vm_name in x:
                self.map[host_name][vm_name][T_name] = T_para
            else:
                self.map[host_name][vm_name] = {T_name: T_para}
        else:
            self.map[host_name] = {vm_name:{T_name:T_para}}