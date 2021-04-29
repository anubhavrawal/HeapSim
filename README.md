# Heap Simulator

## Compile instruction

```
make run
```

OR

```
python3 hsim.py [-h] [-s <value>] [-w] [-v] [-d] --free-list={implicit or explicit} --fit={first or best} <input file>
```

### Required flags:
    --fit= {first/best}
    --free-list={implicit/explicit}

### Usable optional flags:
    -h          prints usage
    -v          is for verbose mode
    -d          will prevent from creating a `output.txt` file and display on screen
    -s <value>  will allow to change the size of initial heap 
    -w          writes the verbose commands into a file and stores into the `verbose` folder

`output.txt` file is creadted on deafult to show the state of the heap.
> `output.txt` will not be created if there is the error on inputfile instruction.


## Input File format Requirement

```
a, 5, 0      // ptr0 = myalloc(5)
f, 0         // myfree(ptr0)
a, 10, 1     // ptr1 = myalloc(10)
r, 20, 1, 2  // ptr2 = myrealloc(ptr1,20)
f, 2         // myfree(ptr2)
```
## Output file format 

```
  0, 0x00000001 // placeholder
  1, 0x00000F98 // header
  2,            // payload
  3,            // payload
  4, 0x00000011 // remaining footer of myalloc(5)
  5, 0x00000F88 // remaining header of free block after myalloc(5)
  6, 0x00000018 // remaining footer of myalloc(10)
  7, 0x00000021 // remaining header of myrealloc(20)
     ......
 10, 0x00000011 // copied payload from word 4 of myrealloc(20)
 11, 0x00000F88 // copied payload from word 5 of myrealloc(20)
     ......
 14, 0x00000021 // remaining footer of myrealloc(20)
 15, 0x00000F60 // remaining header of free block after myrealloc(20)

     ......

998, 0x00000F98 // footer
999, 0x00000001 // placeholder

```


## Test
Few test states are avilable under examples to compare the working program.

Precision of code can be checked by the provided makefiles by using the command.

```
make -f <test_file> -i
```
> Explicit state of heap will not pass all the test cases 


## Notes on Explicit first and best fit:
For these conditions fist footer is collased then header is collased and the new pointers will not be assigned until both collasing are checked and/or completed