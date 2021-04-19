import sys
import math

PERFECT = 1
ERROR = -1
MEM_INCREASE = 2

implicit = False

first_fit = True

verbose = True

class Heap( ):
    def __init__(self):
        self.size = 40
        self.sizemax = 100000
        
        self.memory_block = [ 0xDEADBEEF for x in range(self.size ) ]  
        self.memory_block[0] = 0x1

        self.memory_block[1] = ( ( self.size - 2 ) * 4  )

        self.memory_block[self.size - 2] = self.memory_block[1]
        self.memory_block[self.size - 1] = 0x1

        if implicit == False:
            self.memory_block[2] = 0x0
            self.memory_block[3] = 0x0
            
            self.free_root_head = 1
            self.free_prev_index =  2
            self.free_next_index =  3

        self.free_index = 1

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

            new_header = curr_index + new_block

            self.memory_block[new_header] = mem_remaining

            self.memory_block[footer_loc ] = mem_remaining
            
            #IF Explicit free List
            if implicit == False:
                #print(new_header + 1)
                self.memory_block[new_header + 1 ] = 0x0 
                self.memory_block[new_header + 2 ] = 0x0
                
                self.free_root_head = new_header
                self.free_prev_index = new_header + 1
                self.free_next_index = new_header + 2
            
            return 0
            #------------------------------------------------------------
        else:
            # if first_fit == True:
            #     return 8
            # else:
            #     if (mem_remaining < 8):
            #         return 0
            #     else:
            #         return 8
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
    
    def mem_extender(self, new_size):
        last_end_index = self.size - 1

        if self.mysbrk(new_size//4) == ERROR:
            return ERROR

        self.memory_block[last_end_index] = new_size | 1
        self.memory_block[self.size - 2] = new_size | 1

        self.memory_block[self.size - 1] = 0x1

        free_index = last_end_index
        
        return free_index + 1
    
    def implicit_list(self, new_size):
        free_index = 1
        found = False
        bf_index = -1

        while(self.memory_block[free_index] != 0x1 ):
            #IF the block is free then:
            if self.memory_block[free_index] & 1 ==  0:
            
                #Do we have more memory then we need to store the information
                if self.memory_block[free_index] & ~ 1 > new_size:
                    if first_fit == True:
                        return self.imp_ff(new_size,free_index)
                    else:
                        # if self.memory_block[free_index] & ~ 1 < (new_size +16):
                        #     bf_index = free_index
                        #     break

                        if bf_index == -1:
                            bf_index = free_index

                        elif self.memory_block[free_index] & ~ 1 < self.memory_block[bf_index]:
                            bf_index = free_index
                        
                        # else:
                        #     continue

                        free_index += (self.memory_block[free_index] ) // 4

                #Do we have exact amount of memeory
                elif self.memory_block[free_index] & ~ 1 == new_size:
                    
                    self.memory_block[free_index] = new_size | 1 #  Header allocated memomry
                    self.memory_block[free_index + ((new_size//4)) -1 ] =  new_size | 1 # Footer allocatd memory
                    return free_index + 1
                    
                
                #If not then go the next block
                else:
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
            return self.mem_extender(new_size)
        
        #Case for best_fit
        else:
            #If an appropriate index is found before the end of array
            if bf_index != -1:
                curr_header = bf_index
                new_size += self.practitioner(curr_header, new_size)

                curr_footer = bf_index + ((new_size//4)) - 1

                self.memory_block[curr_header] = new_size | 1
                self.memory_block[curr_footer] = new_size | 1

                return curr_header + 1
            
            #If we hit the end of array but no value appropriate value is found
            #Call sbrk
            else:
                return self.mem_extender(new_size)
    
    #Paramerters:
    #   curr_header         in      index int   ->  is the index of header note
    #   alloc_size          in      words
    def exp_loca_assign(self, alloc_size, curr_header):
        prev_index, next_index = curr_header + 1, curr_header + 2
        
        self.memory_block[curr_header] = alloc_size | 1
        self.memory_block[curr_header + ((alloc_size//4)) - 1] = alloc_size | 1

        
        #self.memory_block[curr_header + 1] = 0x0
        #self.memory_block[curr_header + 2] = 0x0

        return curr_header + 1
    

    def explicit_list(self, new_size):
        curr_header = self.free_root_head
        next_index = self.free_next_index
        
        while(self.memory_block[next_index] != 0x0 ):
            #Is the block free???
            if self.memory_block[curr_header] & 1 ==  0:
                break
            
            #If the block is not free
            else:
                curr_header = self.memory_block[next_index]
                next_index = curr_header + 2
            
        
        new_size += self.practitioner(curr_header,new_size)
        
        return self.exp_loca_assign(new_size, curr_header)

            

    def mymalloc(self, size):
        #header + required size + any possible padding + footer
        new_size =  ( math.ceil(size/8) * 8 ) + 8
        if implicit == True:
            return self.implicit_list(new_size)
        else:
            return self.explicit_list(new_size)



    def print_heap(self):
        for x in range( self.size ):
            #print( str(x) +", " + hex(self.memory_block[x] ).upper() ) 
            print(str(x)+", ", end='')
            if self.memory_block[x] != 0xDEADBEEF :
                print("0x{:08X}".format(self.memory_block[x]) )
            else:
                print()

    def myfree(self, pointer):
        header_index = pointer - 1 # Move 1 step back to reach header
        
        last_footer = -1
        last_header = -1

        
        footer_index = header_index + (self.memory_block[header_index] ) // 4 - 1 #Find the footer index
        #print("For pointer %d the index is %d."%(pointer, footer_index))

        #IF the index next to footer is free
        if (self.memory_block[footer_index + 1]) & 1 == 0 :
            last_footer = footer_index + 1
            footer_index += (self.memory_block[footer_index + 1] ) // 4 
        
        #If the index before header is free
        if (self.memory_block[header_index - 1]) & 1 == 0 :
            last_header = header_index - 1
            header_index -= (self.memory_block[header_index-1] ) // 4

        #Store how much of step we are moving after reaching a new header or footer
        blocksize = ((footer_index - header_index) * 4) + 4

        #Update header then footer index
        self.memory_block[header_index] = blocksize & ~ 1 
        self.memory_block[footer_index] = self.memory_block[header_index]

        if implicit == False:
            if last_footer != -1 and last_header != -1:
                self.memory_block[header_index + 1] = self.memory_block[last_header]
                #self.memory_block[
            
            else:
                self.memory_block[self.free_prev_index] = header_index 

                self.memory_block[header_index + 2] = self.free_next_index
                self.memory_block[header_index + 1] = 0x0

                self.free_root_head = header_index
                self.free_next_index = header_index + 2
                self.free_prev_index = header_index + 1


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
                    print("\n-----------------------------------%s-----------------------------------\n"% (str(command)))
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