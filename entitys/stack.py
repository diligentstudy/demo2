class Stack:
    # 栈是一种线性数据结构，用先进后出或者是后进先出的方式存储数据，栈中数据的插入删除操作都是在栈顶端进行，常见栈的函数操作包括
    def __init__(self):
        self.lst = []

    #向栈顶添加元素
    def push(self,val):
        self.lst.append(val)

    #删除栈顶元素
    def pop(self):
        if self.size() > 0:
            return self.lst.pop()
        else:
            return ""

    # 查看栈顶元素
    def top(self):
        if self.size() >0:
            return self.lst[-1]
        else:
            return ""

    def size(self):
        return len(self.lst)

    def isEmpty(self):
        return self.lst == []

    def getList(self):
        return self.lst

    def clear(self):
        self.lst = []


