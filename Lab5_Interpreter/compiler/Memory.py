from collections import defaultdict


class Memory:

    def __init__(self, name): # memory name
        self.symbols = {}
        self.name = name

    def has_key(self, name):  # variable name
        return name in self.symbols.keys()

    def get(self, name):         # gets from memory current value of variable <name>
        return self.symbols[name]

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.symbols[name] = value


class MemoryStack:

    def __init__(self, memory=Memory("global")): # initialize memory stack with memory <memory>
        self.memories = [memory]
        self.stack_height = 0

    def get_level(self, name):
        i = self.stack_height
        while i >= 0:
            if self.memories[i].has_key(name):
                return i
            i -= 1
        return self.stack_height

    def get(self, name):             # gets from memory stack current value of variable <name>
        level = self.get_level(name)
        return self.memories[level].get(name)

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        self.memories[self.stack_height].put(name, value)

    def set(self, name, value): # sets variable <name> to value <value>
        level = self.get_level(name)
        self.memories[level].put(name, value)

    def push(self, memory): # pushes memory <memory> onto the stack
        self.memories.append(memory)
        self.stack_height += 1

    def pop(self):          # pops the top memory from the stack
        self.memories.pop()
        self.stack_height -= 1
