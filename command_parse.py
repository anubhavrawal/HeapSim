import sys
import getopt

def usage():
    print("usage: python3 main.py [-d] [-h] [-v] --free-list={implicit or explicit} --fit={first or best} <input file>")

def main():
    first_fit = None
    implicit = None
    size = -1
    verbose = False
    filename = ''
    display = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'vhz:', ['free-list=', 'fit='])
    except getopt.GetoptError as err:
        print("Error!!! ")
        print (err)
        usage()
        return

    print('opts:', opts)
    
    for opt, arg in opts:
        if opt in ('-h'):
            usage()
            return

        elif opt in ('-v'):
            print('Verbose')
        
        elif opt in ('--free-list'):
            if arg == 'implicit':
                implicit= True
            elif arg == 'explicit':
                implicit =False
            else:
                print('Error in implicit!!!')
                usage()
                return
            print('implicit:',implicit)
        
        elif opt in ('--fit'):
            if arg == 'first':
                first_fit= True
            elif arg == 'best':
                first_fit =False
            else:
                print('Error in fit!!!')
                usage()
                return

            print('fit=', first_fit)
        
        elif opt in ("-d"):
            display = True
        
        elif opt in ('-z'):
            size = arg
        
        else:
            filename = arg
    
    print(args)
    #filename = sys.argv[-1]
    print(filename)
            


main()