import sys
import math

PERFECT = 1
ERROR = -1
MEM_INCREASE = 2

class Heap( ):
    def __init__(self):
        self.size = 16
        self.sizemax = 100000
        
        self.memory_block = [ 0x0 for x in range(self.size ) ]  
        self.memory_block[0] = 0x1

        self.memory_block[1] = ( ( self.size - 2 ) * 4  )

        self.memory_block[self.size - 2] = self.memory_block[1]
        self.memory_block[self.size - 1] = 0x1

    def mysbrk(self, size):
        if (size > self.size):
            if (self.size + size) < self.sizemax:
                self.memory_block += [0x0] *size
                self.size += size

                return PERFECT
            else:
                return ERROR
        return ERROR


    def mymalloc(self, size):
        free_index = 1
        next_free_index = 1
        
        new_size =  ( math.ceil(size/8) * 8 ) + 8

        while(1):
            if self.memory_block[free_index] & 1 ==  0:

                #IF we have enough memory to store the information
                if self.memory_block[free_index] & ~ 1 >= new_size:   
                    tmp = self.memory_block[free_index] - new_size

                    new_block = new_size // 4

                    #If we have a avilable free space of 16 or greater
                    #Then only partition the memmory
                    if ( tmp >= 16):

                        #Updateing the free header and footer:
                        tmp_size = self.memory_block[free_index] - new_size

                        footer_loc = free_index + (self.memory_block[free_index] ) // 4 - 1


                        self.memory_block[free_index + new_block] = tmp

                        self.memory_block[footer_loc ] = tmp

                        #------------------------------------------------------------
                    
                    else:
                        new_size = new_size + 8
                
                    
                    self.memory_block[free_index] = new_size | 1 #  Header allocated memomry

                    self.memory_block[free_index + ((new_size//4) - 1)] =  new_size | 1 # Footer allocatd memory

                    return free_index + 1
                
                else:
                    #self.memory_block[self.size - 1] = 0x0

                    last_footer_index = self.size - 2
                    
                    self.mysbrk(new_size + 8)
 
                    self.memory_block[last_footer_index + 1] += 

                    self.memory_block[self.size - 1] = 0x1

                    continue

            else:
                free_index += (self.memory_block[free_index] ) // 4
                continue


    def print_heap(self):
        for x in range( self.size ):
            print( str(x) +", " +  "0x" + hex(self.memory_block[x] ).upper() ) 

    def myfree(self, pointer):
        coalesce = False
        header_index = pointer - 1 
        footer_index = header_index + (self.memory_block[header_index] ) // 4 - 1

        if (self.memory_block[footer_index + 1]) & 1 == 0 :
            footer_index += (self.memory_block[footer_index + 1] ) // 4 
        
        if (self.memory_block[header_index - 1]) & 1 == 0 :
            header_index -= (self.memory_block[header_index-1] ) // 4

        blocksize = ((footer_index - header_index) * 4) + 4
        self.memory_block[header_index] = blocksize & ~ 1 #Updating header Index
        self.memory_block[footer_index] = self.memory_block[header_index] #Updating footer Index

        return
    
    def myrealloc(self, pointer, size):
        pass

    
def main():
    memory = Heap()

   
    pointer = {}

    
    with open( sys.argv[1] ) as file:
        for line in file.readlines():
            if (line[0] == "#"):
                continue

            line = line.split('\n')[0]
            line = line.strip()

            command = line.split(',')
            
            if command[0] == 'a':
                location = memory.mymalloc( int(command[1]) )
                pointer[ int(command[2]) ] = location

                print(pointer)
            
            elif  command[0] == 'f':
                memory.myfree( pointer[ int(command[1]) ] )
            
            elif command[0] == 'r':
                location = memory.myrealloc( pointer[int(command[2])] , int( command[1] ) ) #old_pointer,size

                pointer[ int(command[3]) ] = location
    
    memory.print_heap()
            
main()