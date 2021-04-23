Date: 04/19/2021
Class: CS5541
Assignment: Heap Simulator
Author(s): Anubhav Rawal (Altan)
 
Compile command and run:
	`make run`

        OR

    `python3 main.py [-v] [-d] --free-list={implicit or explicit} --fit={first or best} <input file>`

Notes:
    filename must always be the last argument. There is no warranty if the flags are used after the filename
    
    Required flags:
        --fit= {first/best}
        --free-list={implicit/explicit}

    Usable optional flags:
        -h prints usage
        -v is for verbose mode
        -d will prevent from creating a `output.txt` file and display on screen
        -s <value> will allow to change the size of initial heap 
        -w writes the verbose commands into a file and stores into the `verbose` folder

    output.txt file is creadted on deafult to show the state of the heap.
    No output.txt will be created if there is the error on the code.

    ***************************************************************************************************************
    Explicit first and best fit:
        for these conditions fist footer is collased then header is collased and the new pointers will not be assigned until both collasing are checked and/or completed
        Hence Produces a bit of differnt pointer than the sample given.
        So Test9 needs to be checked for the avilable file rather than it's content
    ***************************************************************************************************************
 
References: 
    Zander Thannhauser
