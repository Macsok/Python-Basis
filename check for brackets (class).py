#define class which stores string to operate on
class Counter:
    __str = ''
    #constructor
    def __init__(self, string):
        self.__str = string

    #check whether every symbol has a 'pair'
    def check_for(self, start_char, end_char):
        stack = []
        #add on stack if opening one, pop if closing one
        for i in range(len(self.__str)):
            if self.__str[i] == start_char:
                stack.append('c')
            if self.__str[i] == end_char:
                if len(stack) > 0:
                    stack.pop()
                #if wants to pop from empty stack
                else:
                    return False
        #if stack is empty then test went well
        if len(stack) == 0:
            return True
        else: 
            return False
    
    #check for common brackets correctness
    def check_for_common(self):
        if self.check_for('(', ')') and self.check_for('[', ']') and self.check_for('{', '}'):
            return True
        else:
            return False

        
Obj = Counter('()[]abcd{}')
print(Obj.check_for_common())