
class utils():
    def add_map(self, host_name, vm_name, T_para, T_name):
        if host_name in self.map:
            x = self.map[host_name]
            if vm_name in x:
                self.map[host_name][vm_name][T_name] = T_para
            else:
                self.map[host_name][vm_name] = {T_name: T_para}
        else:
            self.map[host_name] = {vm_name:{T_name:T_para}}