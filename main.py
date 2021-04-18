import sys
import math

PERFECT = 1
ERROR = -1
MEM_INCREASE = 2

implecit = True

first_fit = True

verbose = False

class Heap( ):
    def __init__(self):
        self.size = 1000
        self.sizemax = 100000
        
        self.memory_block = [ 0xDEADBEEF for x in range(self.size ) ]  
        self.memory_block[0] = 0x1

        self.memory_block[1] = ( ( self.size - 2 ) * 4  )

        self.memory_block[self.size - 2] = self.memory_block[1]
        self.memory_block[self.size - 1] = 0x1

    def mysbrk(self, size):
        if (self.size + size) < self.sizemax:
            self.memory_block += [0xDEADBEEF] *size
            self.size += size

            return PERFECT
        else:
            return ERROR
    
    #Paramerters:
    #   mem_remaining   in      bytes
    #   word_size        in      words
    def practitioner(self, curr_index, word_size):

        mem_remaining = self.memory_block[curr_index] - word_size

        #If we have a avilable free space of 16 or greater
        #Then only partition the memmory
        if ( mem_remaining >= 16):
            #Updateing the splited header and footer:
            #tmp_size = self.memory_block[curr_index] - word_size
            new_block = word_size // 4

            footer_loc = curr_index + (self.memory_block[curr_index] ) // 4 - 1

            self.memory_block[curr_index + new_block] = mem_remaining

            self.memory_block[footer_loc ] = mem_remaining
            
            return 0
            #------------------------------------------------------------
        else:
            return 8


    def imp_ff(self, new_size, free_index):
        # mem_remaining = self.memory_block[free_index] - new_size

        # #If we have a avilable free space of 16 or greater
        # #Then only partition the memmory
        # if ( mem_remaining >= 16):

        #     self.practitioner(free_index, new_size, mem_remaining)
        
        # else:
        #     new_size = new_size + 8

        new_size += self.practitioner(free_index, new_size)
    
        self.memory_block[free_index] = new_size | 1 #  Header allocated memomry

        #for index in range(self.memory_block[free_index] //4 - 2 ):
        #    self.memory_block[free_index +index +1] =  0x0

        self.memory_block[free_index + ((new_size//4)) -1 ] =  new_size | 1 # Footer allocatd memory

        return free_index + 1
    


    def mymalloc(self, size):
        free_index = 1
        found = False
        bf_index = -1
        #next_free_index = 1
        
        #header + required size + any possible padding + footer
        new_size =  ( math.ceil(size/8) * 8 ) + 8

        while(self.memory_block[free_index] != 0x1 ):

            #IF the block is free then:
            if self.memory_block[free_index] & 1 ==  0:
            
                #Do we have enough memory to store the information
                if self.memory_block[free_index] & ~ 1 > new_size:
                    if first_fit == True:
                        return self.imp_ff(new_size,free_index)
                    else:
                        if bf_index == -1:
                            bf_index = free_index

                        elif self.memory_block[free_index] & ~ 1 < self.memory_block[bf_index]:
                            bf_index = free_index
                        
                        else:
                            continue

                elif self.memory_block[free_index] & ~ 1 == new_size:
                    #if first_fit == True:
                    
                    self.memory_block[free_index] = new_size | 1 #  Header allocated memomry
                    self.memory_block[free_index + ((new_size//4)) -1 ] =  new_size | 1 # Footer allocatd memory
                    return free_index + 1
                    
                
                #If not then go the next block
                else:
                    """ 
                    #self.memory_block[self.size - 1] = 0x0
                    last_footer_index = self.size - 2
                    
                    self.mysbrk(new_size + 8)
                    self.memory_block[last_footer_index + 1] += 1
                    self.memory_block[self.size - 1] = 0x1

                    continue 
                    """
                    free_index += (self.memory_block[free_index] ) // 4
                    continue
                    

            
            #IF the block is not free 
            #Then go the end of the current block +1
            #This will be header of following block
            else:
                free_index += (self.memory_block[free_index] ) // 4
                continue
        
        # If we have hit the end of the array and do not have enough space
        # to meet the requested space requirements
        if first_fit == True:
            last_end_index = self.size - 1
            
            ret_val = self.mysbrk(new_size//4)

            if ret_val == ERROR:
                return ERROR

            self.memory_block[last_end_index] = new_size | 1
            self.memory_block[self.size - 2] = new_size | 1

            self.memory_block[self.size - 1] = 0x1

            free_index = last_end_index
            return free_index
        
        #Case for best_fit
        else:
            if bf_index != -1:
                curr_header = bf_index
                curr_footer = bf_index + ((new_size//4)) - 1

                self.memory_block[curr_header] = new_size | 1
                self.memory_block[curr_footer] = new_size | 1

                return curr_header




    def print_heap(self):
        for x in range( self.size ):
            #print( str(x) +", " + hex(self.memory_block[x] ).upper() ) 
            print(str(x)+", ", end='')
            if self.memory_block[x] != 0xDEADBEEF :
                print("0x{:08X}".format(self.memory_block[x]) )
            else:
                print()

    def myfree(self, pointer):
        #coalesce = False #Flag for calase touggle

        header_index = pointer - 1 # Move 1 step back to reach header
        
        footer_index = header_index + (self.memory_block[header_index] ) // 4 - 1 #Find the footer index
        #print("For pointer %d the index is %d."%(pointer, footer_index))

        #IF the index next to footer is free
        if (self.memory_block[footer_index + 1]) & 1 == 0 :
            footer_index += (self.memory_block[footer_index + 1] ) // 4 
        
        #If the index before header is free
        if (self.memory_block[header_index - 1]) & 1 == 0 :
            header_index -= (self.memory_block[header_index-1] ) // 4

        #Store how much of step we are moving after reaching a new header or footer
        blocksize = ((footer_index - header_index) * 4) + 4

        #Update header then footer index
        self.memory_block[header_index] = blocksize & ~ 1 
        self.memory_block[footer_index] = self.memory_block[header_index]

        return
    
    def myrealloc(self, pointer, size):
        old_block_size = (self.memory_block[pointer - 1] //4)
        
        requested_block = (( math.ceil(size/8) * 8 ) + 8 )//4

        if size == 0:
            self.myfree(pointer)
            return 0
        # elif old_block_size > requested_block:
        #     return pointer

        new_ptr = self.mymalloc(size)

        if new_ptr == ERROR:
            return ERROR
       
        if old_block_size < requested_block:
            for index in range(old_block_size - 2):
                self.memory_block[new_ptr + index] = self.memory_block[pointer + index]
            
            self.myfree(pointer)
            return new_ptr
        
        else:
            #old_block_size > requested_block:
            return pointer
            



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
                if location == ERROR:
                    return
                pointer[ int(command[2]) ] = location

                #print(pointer)
                if verbose == True:
                    print("\n-----------------------------------After Allocation-----------------------------------\n")
                    memory.print_heap()
                    print("\n--------------------------------------------------------------------------------------\n")
               

            elif  command[0] == 'f':
                memory.myfree( pointer[ int(command[1]) ] )

                #print("Pointer:", command[1], "with index:", pointer[ int(command[1]) ])
                if verbose == True:
                    print("\n-----------------------------------After Free-----------------------------------------\n")
                    memory.print_heap()
                    print("\n--------------------------------------------------------------------------------------\n")

            elif command[0] == 'r':
                location = memory.myrealloc( pointer[int(command[2])] , int( command[1] ) ) #old_pointer,size

                if location == ERROR:
                    return

                pointer[ int(command[3]) ] = location
                
                if verbose == True:
                    print("\n-----------------------------------After Realloc--------------------------------------\n")
                    memory.print_heap()
                    print("\n--------------------------------------------------------------------------------------\n")
    
    if verbose == False:
        memory.print_heap()
            
main()