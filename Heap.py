import math

PERFECT = 1
ERROR = -1
MEM_INCREASE = 2

class Heap( ):
    def __init__(self, imp, fit,verb, init_heap_size = 1000):
        self.implicit = imp
        self.first_fit = fit
        self.verbose = verb

        self.size = init_heap_size
        self.sizemax = 100000
        
        self.memory_block = [ 0xDEADBEEF for x in range(self.size ) ]  
        self.memory_block[0] = 0x1

        self.memory_block[1] = ( ( self.size - 2 ) * 4  )

        self.memory_block[self.size - 2] = self.memory_block[1]
        self.memory_block[self.size - 1] = 0x1

        if self.implicit == False:
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
            print(sys.argv[0] + ": total heap capacity reached! (100000 words)")
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
            new_block = word_size // 4

            footer_loc = curr_index + (self.memory_block[curr_index] ) // 4 - 1

            new_header = curr_index + new_block

            self.memory_block[new_header] = mem_remaining

            self.memory_block[footer_loc ] = mem_remaining
            
            #IF Explicit free List
            if self.implicit == False:
            
                #moving the pointers to the new block
                self.memory_block[new_header + 1 ] = self.memory_block[curr_index + 1] 
                self.memory_block[new_header + 2 ] = self.memory_block[curr_index + 2]
                
                if self.free_root_head == curr_index:
                    self.free_root_head = self.memory_block[self.free_root_head+2]

                #Removing the element from the list
                #Updating the previous and next pointer origins
                if self.memory_block[curr_index + 1] != 0x0:
                    self.memory_block[self.memory_block[curr_index + 1] + 2] = new_header 

                if self.memory_block[curr_index + 2] != 0x0:
                    self.memory_block[self.memory_block[curr_index + 2] + 1] = new_header 

                
                
                self.free_root_head = new_header
            
            return 0
            #------------------------------------------------------------
        else:
            
            if self.implicit ==False:
                if self.memory_block[curr_index + 1] != 0x0:
                    self.memory_block[self.memory_block[curr_index + 1] + 2] = self.memory_block[curr_index + 2] #prev -> next
                    
                if self.memory_block[curr_index + 3] != 0x0:
                    self.memory_block[self.memory_block[curr_index + 2] + 1] = self.memory_block[curr_index + 1] #next -> prev
                
                if self.free_root_head == curr_index:
                    self.free_root_head = self.memory_block[self.free_root_head+2]

            return 8


    def imp_ff(self, new_size, free_index):

        new_size += self.practitioner(free_index, new_size)
    
        self.memory_block[free_index] = new_size | 1 #  Header allocated memomry

        self.memory_block[free_index + ((new_size//4)) -1 ] =  new_size | 1 # Footer allocatd memory

        return free_index + 1
    
    def mem_extender(self, new_size):
        last_end_index = self.size - 1

        if self.mysbrk(new_size//4) == ERROR:
            return ERROR

        self.memory_block[last_end_index] = new_size | 1
        self.memory_block[self.size - 2] = new_size | 1

        self.memory_block[self.size - 1] = 0x1
        
        return last_end_index + 1
    
    def implicit_list(self, new_size):
        free_index = 1
        found = False
        bf_index = -1

        while(self.memory_block[free_index] != 0x1 ):
            #IF the block is free then:
            if self.memory_block[free_index] & 1 ==  0:
            
                #Do we have more memory then we need to store the information
                if self.memory_block[free_index] & ~ 1 > new_size:
                    if self.first_fit == True:
                        return self.imp_ff(new_size,free_index)
                        
                    else:
                        if bf_index == -1:
                            bf_index = free_index

                        elif self.memory_block[free_index] & ~ 1 < self.memory_block[bf_index]:
                            bf_index = free_index


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
        if self.first_fit == True:
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

        return curr_header + 1
    

    def explicit_list(self, new_size):
        curr_header = self.free_root_head
        best_index = -1
        
        while( curr_header != 0x0):
            #Do we have more memory then we need to store the information
            if self.memory_block[curr_header] & ~ 1 > new_size:
                if self.first_fit == True:
                    best_index = curr_header
                    break
                    #found = True
                else:
                    if best_index == -1:
                        best_index = curr_header

                    elif self.memory_block[curr_header] & ~ 1 < self.memory_block[best_index]:
                        best_index = curr_header
                    
                    curr_header = self.memory_block[curr_header + 2]
        
            elif self.memory_block[curr_header] & ~ 1 == new_size:
                return self.exp_loca_assign(new_size, curr_header)

            #If we do not have enough space to store the information
            else:
                curr_header = self.memory_block[curr_header + 2]
            
        
        if best_index == -1:
            return self.mem_extender(new_size)


        new_size += self.practitioner(best_index,new_size)
        
        return self.exp_loca_assign(new_size, best_index)

            

    def mymalloc(self, size):
        #Sum of:
        #header + required size + any possible padding + footer
        new_size =  ( math.ceil(size/8) * 8 ) + 8
        if self.implicit == True:
            return self.implicit_list(new_size)
        else:
            return self.explicit_list(new_size)

    def print_heap(self,verb):
        for x in range( self.size ):
            if verb == True:
                if self.implicit == False:
                    if x == self.free_root_head:
                        print("**", end="")

            print(str(x)+", ", end='')
            if self.memory_block[x] != 0xDEADBEEF :
                print("0x{:08X}".format(self.memory_block[x]) )
            else:
                print()
    
    def write_heap(self, outname='output.txt'):
        with open(outname, 'w') as out:
            for x in range( self.size ):
                out.write(str(x)+", ")
                if self.memory_block[x] != 0xDEADBEEF :
                    out.write("0x{:08X}\n".format(self.memory_block[x]) )
                else:
                    out.write("\n")

    def myfree(self, pointer):
        header_index = pointer - 1 # Move 1 step back to reach header
        
        collase_footer = -1

        
        footer_index = header_index + (self.memory_block[header_index] ) // 4 - 1 #Find the footer index

        #IF the index next to footer is free
        if (self.memory_block[footer_index + 1]) & 1 == 0 :
            
            if self.implicit == False:
                
                #Move the pointer in such a way that the current block is skipped in the memory
                if self.memory_block[footer_index + 2] != 0x0:
                    self.memory_block[self.memory_block[footer_index + 2] + 2] = self.memory_block[footer_index + 3] #prev -> next
                
                if self.memory_block[footer_index + 3] != 0x0 and footer_index+3 != self.size:
                    self.memory_block[self.memory_block[footer_index + 3] + 1] = self.memory_block[footer_index + 2] #next -> prev
                
                if footer_index+1 == self.free_root_head or footer_index+2 == self.free_root_head:
                    self.free_root_head = self.memory_block[footer_index + 3]

            footer_index += (self.memory_block[footer_index + 1] ) // 4

            
        #If the index before header is free
        if (self.memory_block[header_index - 1]) & 1 == 0 :
            header_index -= (self.memory_block[header_index-1] ) // 4

            if self.implicit == False:
                #Move the pointer in such a way that the current block is skipped in the memory
                if self.memory_block[header_index + 1] > 0x0:
                    self.memory_block[self.memory_block[header_index + 1] + 1] = self.memory_block[header_index + 2] #prev -> next
                
                if self.memory_block[header_index + 2] > 0x0:
                    self.memory_block[self.memory_block[header_index + 2]+1 ] = self.memory_block[header_index + 1] #next -> prev
                
                if header_index == self.free_root_head:
                    self.free_root_head = self.memory_block[header_index + 2]
            
        
        #The always case/ case 1 for explicit list 
        if self.implicit == False:

            #Check if the rood head is not set
            if self.free_root_head != 0x0:
                    self.memory_block[self.free_root_head + 1] = header_index 
            
            self.memory_block[header_index + 2] = self.free_root_head
                
            self.memory_block[header_index + 1] = 0x0

            self.free_root_head = header_index

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

        new_ptr = self.mymalloc(size)

        if new_ptr == ERROR:
            return ERROR
       
        if old_block_size < requested_block:
            for index in range(old_block_size - 2):
                self.memory_block[new_ptr + index] = self.memory_block[pointer + index]
            
            self.myfree(pointer)
            return new_ptr
        
        else:
            return pointer