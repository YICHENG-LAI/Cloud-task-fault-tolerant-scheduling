import numpy as np
import random

class Cloudlets():
    def __init__(self):
        self.list = {}
        print('Start generating cloudlets...')

    # randomly generate indepent task list as t_n:(arrival, deadline, length)
    # length [1,5] * 1e5 MIPS
    # VM 1000 MIPS
    def generate_ind(self,num_task, VM = None):
        tlist = {}
        time = 0 # initial runtime
        VM = 1000 # assume MIPS_VM = 1000 MIPS
        for i in range(num_task):
            length = random.randint(1,5) * 1e5
            runtime = length / VM
            arrival = time + random.randint(0,10)
            deadline = arrival + random.randint(10,100) * round(runtime)
            task_name = 't' + str(i)
            time = arrival
            tlist[task_name] = (arrival, deadline, length)
            self.list[task_name] = (arrival, deadline, length)
        print(str(num_task) + ' Independent cloudlets generated ...')
        return self.list

    # randomly generate dependent task list
    def generate_d(self,num_task, VM = None):
        tlist = {}
        print('Dependent cloudlets generated !')
        return tlist


if __name__ == "__main__":
    num_task = 10
    cloudlets = Cloudlets()
    tasks = cloudlets.generate_ind(num_task)
    print(tasks)
    a,b,c = tasks['t0']
    print(a,b,c)