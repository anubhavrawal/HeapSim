import sys
import math

PERFECT = 1
ERROR = -1
MEM_INCREASE = 2

class Heap( ):
    def __init__(self):
        self.size = 20
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
        #next_free_index = 1
        
        #header + required size + any possible padding + footer
        new_size =  ( math.ceil(size/8) * 8 ) + 8

        while(1):
            #IF the block is free then:
            if self.memory_block[free_index] & 1 ==  0:
            
                #Do we have enough memory to store the information
                if self.memory_block[free_index] & ~ 1 >= new_size:   
                    tmp = self.memory_block[free_index] - new_size

                    new_block = new_size // 4

                    #If we have a avilable free space of 16 or greater
                    #Then only partition the memmory
                    if ( tmp >= 16):

                        #Updateing the splited header and footer:
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
                

                # If we have hit the end of the array and do not have enough space
                # to meet the requested space requirements
                #Check with Zander
                elif self.memory_block[free_index + (self.memory_block[free_index] ) // 4 + 1 ] == 0X1:
                    last_footer_index = self.size - 2
                    
                    self.mysbrk(new_size + 8)
                    self.memory_block[last_footer_index + 1] += 1
                    self.memory_block[self.size - 1] = 0x1

                    continue

                
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


    def print_heap(self):
        for x in range( self.size ):
            #print( str(x) +", " + hex(self.memory_block[x] ).upper() ) 
            print(str(x)+", "+ "0x{:08X}".format(self.memory_block[x]) )

    def myfree(self, pointer):
        #coalesce = False #Flag for calase touggle

        header_index = pointer - 1 # Move 1 step back to reach header
        
        footer_index = header_index + (self.memory_block[header_index] ) // 4 - 1 #Find the footer index
        print("For pointer %d the index is %d."%(pointer, footer_index))

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
        #Adjust and find header and footer of current block 
        curr_head = pointer - 1
        curr_block_size = self.memory_block[curr_head] & ~ 1
        curr_footer = curr_head + (self.memory_block[curr_head] ) // 4 - 1

        requested_size = ( math.ceil(size/8) * 8 ) + 8
        #Convert size to blocks
        requested_block = requested_size // 4
        #If we could fit in the information in the same block
        #Return the same pointer
        if requested_size == self.memory_block[curr_head] :
            return pointer
        #Calculate extra required block
        extra_block =  requested_block - curr_block_size//4

        #If the memory_block next to footer IS free
        if (self.memory_block[curr_footer + 1]) & 1 == 0 :

            #The header will always store the reuired amount of bytes
            self.memory_block[curr_head] = requested_size | 1

            #temporary next memory block's header and footer
            next_header = curr_footer + 1
            next_footer = next_header + (self.memory_block[next_header] ) // 4 - 1
             

            #If we have just the extra space
            if ((self.memory_block[curr_footer + 1] // 4)  == (extra_block)):
                
                #Just update footer
                self.memory_block[next_footer] = self.memory_block[curr_head]

                #Return the pointer
                return curr_head + 1

            #If we have space for more than required size + 2 placeholder
            elif (self.memory_block[curr_footer + 1] // 4)  > (extra_block + 2):
                next_header = curr_head + requested_block
                curr_footer = next_header - 1

                self.memory_block[curr_footer] = self.memory_block[curr_head]
                
                new_tmp_size = self.memory_block[next_footer] - extra_block * 8

                self.memory_block[next_header] = new_tmp_size
                self.memory_block[next_footer] = new_tmp_size

                return curr_head + 1
            
            #If not free that memory block and look for a new one
            else:
                self.myfree(pointer)
                tmp_pointer = self.mymalloc(size)
                return tmp_pointer
        
        #If the memory next to free IS NOT free
        #free that memory block and look for a new one
        else:
            self.myfree(pointer)
            tmp_pointer = self.mymalloc(size)
            return tmp_pointer



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

                #print(pointer)

                print("\n-----------------------------------After Allocation-----------------------------------\n")
                memory.print_heap()
                print("\n--------------------------------------------------------------------------------------\n")
            
            elif  command[0] == 'f':
                memory.myfree( pointer[ int(command[1]) ] )

                #print("Pointer:", command[1], "with index:", pointer[ int(command[1]) ])
                print("\n-----------------------------------After Free-----------------------------------------\n")
                memory.print_heap()
                print("\n--------------------------------------------------------------------------------------\n")

            elif command[0] == 'r':
                location = memory.myrealloc( pointer[int(command[2])] , int( command[1] ) ) #old_pointer,size

                pointer[ int(command[3]) ] = location
                
                print("\n-----------------------------------After Realloc--------------------------------------\n")
                memory.print_heap()
                print("\n--------------------------------------------------------------------------------------\n")
    
    #memory.print_heap()
            
main()