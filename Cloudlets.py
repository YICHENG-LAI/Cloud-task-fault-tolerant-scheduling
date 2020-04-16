import numpy as np
import random

class Cloudlets():
    def __init__(self):
        self.list = {}
        print('Start generating cloudlets...')

    # randomly generate indepent task list as t_n:(arrival, deadline, length)
    # length [1,5] * 1e5 MIPS
    # VM 1000 MIPS
    def generate_ind(self, num_task, VM = None):
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
    def generate_d(self, beta, VM = None):
        parent = {}
        potential = [] # potential parent cloudlets
        for i in self.list:
            num_po = len(potential)
            if num_po < 2:
                potential.append(i+'_P') 
                continue
            # random number of parent for a cloudlet [0,1,2]
            tmp = random.randint(1,100)
            rand_id = np.arange(num_po)
            np.random.shuffle(rand_id)
            if tmp < (1-beta) * 100: continue
            elif tmp <= 90:
                # rand_id = np.random.randint(num_po,size=1)
                parent[i+'_P'] = [potential[rand_id[0]]]
                parent[i+'_B'] = [potential[rand_id[0]]]
            else:
                parent[i+'_P'] = [potential[rand_id[0]],potential[rand_id[1]]]
                parent[i+'_B'] = [potential[rand_id[0]],potential[rand_id[1]]]
            potential.append(i+'_P')
        print('Dependent cloudlets generated !')
        return parent


if __name__ == "__main__":
    num_task = 10
    cloudlets = Cloudlets()
    tasks = cloudlets.generate_ind(num_task)
    parent = cloudlets.generate_d(0.2)
    print(tasks)
    print(parent)