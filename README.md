# Heap Simulator

## Compile instruction

```
make run
```

OR

```
python3 hsim.py [-v] [-d] --free-list={implicit or explicit} --fit={first or best} <input file>
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
> `output.txt` will not be created if there is the error on the code.


## Input File format Requirement

```
    a, 5, 0      // ptr0 = myalloc(5)
    f, 0         // myfree(ptr0)
    a, 10, 1     // ptr1 = myalloc(10)
    r, 20, 1, 2  // ptr2 = myrealloc(ptr1,20)
    f, 2         // myfree(ptr2)
```

## Notes on Explicit first and best fit:
For these conditions fist footer is collased then header is collased and the new pointers will not be assigned until both collasing are checked and/or completed

### Test

```
make -f <test_file> -i
```