import sys
import os
import math

from Heap import *

def usage():
    print("usage: python3 hsim.py [-h] [-v] [-w] [-z <size>] [-d] --free-list={implicit or explicit} --fit={first or best} <input file>")

def main():
    #input flags set to deafult
    implicit = None
    fit = None
    verbose = False
    filename = ''
    display = False
    wrt_verb = False

    init_size = -1

    #Pasrse the command line args and assign respective values
    for _e in range(1, len(sys.argv)):
        try: 
            if sys.argv[_e][0] == '-':
                if sys.argv[_e] == '-h':
                    usage()
                    return
                
                elif sys.argv[_e][1] == '-':
                    cmp_txt = sys.argv[_e].split('=')
                    
                    if cmp_txt[0] == '--free-list':
                        if cmp_txt[1] == 'implicit':
                            implicit = True
                        elif cmp_txt[1] == 'explicit':
                            implicit = False
                        else:
                            usage()
                            return
                    
                    elif cmp_txt[0] == '--fit':
                        if cmp_txt[1] == 'best':
                            fit = False
                        elif cmp_txt[1] == 'first':
                            fit = True
                        else:
                            usage()
                            return
                elif sys.argv[_e] == '-v':
                    verbose = True
                
                elif sys.argv[_e] == '-w':
                    
                    if not os.path.exists('verbose'):
                        os.makedirs('verbose')

                    wrt_verb = True
                
                elif sys.argv[_e] == '-d':
                    display = True

                elif sys.argv[_e] == '-z':
                    init_size = int( sys.argv[_e +1] )
                else:
                    usage()
                    return
            else:
                filename = sys.argv[_e]
        
        except:
            usage()
            return
    
    if (fit is None) or (implicit is None):
        usage()
        return
    
    if (filename == '') or (filename.isspace()):
        print("Bad Filename.")
        usage()
        return
    try:
        f = open(filename, 'rb')
    except OSError:
        print(filename)
        print("Bad file.")
        usage()
        return

    if init_size == -1:
        memory = Heap(implicit,fit,verbose)
    
    else:
        memory = Heap(implicit,fit,verbose, init_size)

    pointer = {}
    
    
    with open( filename ) as file:
        command_counter = 1
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

                if verbose:
                    if not wrt_verb :
                        print("\n-----------------------------------%s-----------------------------------\n"% (str(command)))
                        memory.print_heap(verbose)
                        print("\n--------------------------------------------------------------------------------------\n")
                    else:
                        memory.write_heap("verbose/%d. \"%s\".txt "%(command_counter,','.join(command)) )

            

            elif  command[0] == 'f':
                if memory.myfree( pointer[ int(command[1]) ] ) ==ERROR:
                    return

                if verbose:
                    if not wrt_verb :
                        print("\n-----------------------------------%s-----------------------------------\n"% (str(command)))
                        memory.print_heap(verbose)
                        print("\n--------------------------------------------------------------------------------------\n")
                    else:
                        memory.write_heap("verbose/%d. \"%s\".txt "%(command_counter,','.join(command)) )

            elif command[0] == 'r':
                location = memory.myrealloc( pointer[int(command[2])] , int( command[1] ) ) #old_pointer,size

                if location == ERROR:
                    return

                pointer[ int(command[3]) ] = location
                
                if verbose:
                    if not wrt_verb :
                        print("\n-----------------------------------%s-----------------------------------\n"% (str(command)))
                        memory.print_heap(verbose)
                        print("\n--------------------------------------------------------------------------------------\n")
                    else:
                        memory.write_heap("verbose/%d. \"%s\".txt "%(command_counter,','.join(command)) )

            command_counter+=1
    
    if not verbose:
        if display:
            memory.print_heap(verbose)
        else:
            memory.write_heap()
          
main()