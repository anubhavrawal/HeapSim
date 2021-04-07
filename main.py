import math

PERFECT = 1

class Block:
    def __int__(self, header, payload, footer):
        self.__header = header
        self.__payload = payload
        self.__footer = footer
    
    def get_header(self):
        return self.__header
    
    def get_payload(self):
        return self.__payload
    
    def get_footer(self):
        return self.__footer
    
    def set_payload(self, payload):
        self.__payload = payload
    
    def set_header(self,header):
        self.__header = header
    
    def set_footer(self,footer):
        self.__footer = footer


class Heap:
    def __int__(self):
        self.curr_head =  1
        self.curr_footer = 2

        self.size = 1000
        self.sizemax = 100000

    def mysbrk(self, size):
        if (size > self.size):
            self.size =  self.size + size + 1
            if self.size > self.sizemax:
                return -1


    def mymalloc(self, size):
        if size < self.size:
            new_size =  (math.ceil(size,8) * 8 ) / 4
            
            self.curr_head = (new_size + 2) | 1    

            self.curr_footer =  self.curr_head + new_size + 1
            new_block =  Block(self.curr_head, new_size, self.curr_footer)

            return PERFECT

        else:
            return self.mysbrk(size)
                

    def free(self, pointer):
        if (pointer.get_header() & 1 == 0):
            return -1

        pointer.set_header( pointer.get_header() & ~ 1 )

        pointer.set_footer( pointer.get_footer() & ~ 1 )

        return
    
    def realloc(self, pointer, size):


        


def main():
    memory = Heap()

    


    

        

