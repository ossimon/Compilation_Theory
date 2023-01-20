from collections import defaultdict


class Memory:

    def __init__(self, name): # memory name
        self.symbols = defaultdict()
        self.name = name

    def has_key(self, name):  # variable name
        return self.symbols[name] is not None

    def get(self, name):         # gets from memory current value of variable <name>
        return self.symbols[name]

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.symbols[name] = value


class MemoryStack:

    def __init__(self, memory=None): # initialize memory stack with memory <memory>
        self.memories = [memory]
        self.stack_height = 0

    def get(self, name):             # gets from memory stack current value of variable <name>
        i = self.stack_height
        while i > 0:
            if self.memories[i][name] is not None:
                return self.memories[i][name]
            i -= 1
        return None

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        self.memories[self.stack_height].put(name, value)

    def set(self, name, value): # sets variable <name> to value <value>
        self.memories[self.stack_height].put(name, value)

    def push(self, memory): # pushes memory <memory> onto the stack
        self.memories.append(memory)

    def pop(self):          # pops the top memory from the stack
        self.memories.pop()
