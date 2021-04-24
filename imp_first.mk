all: test1 test2 test3 test4 test5 test6 test7 test8 test10 test11 test12 test13

compile1:
	python3 hsim.py --free-list=implicit --fit=first examples/1/in.txt 

test1: compile1
	diff output.txt examples/1/implicit.first.txt

compile2:
	python3 hsim.py --free-list=implicit --fit=first examples/2/in.txt 

test2: compile2
	diff output.txt examples/2/implicit.first.txt

compile3:
	python3 hsim.py --free-list=implicit --fit=first examples/3/in.txt 

test3:compile3
	diff output.txt examples/3/implicit.first.txt

compile4:
	python3 hsim.py --free-list=implicit --fit=first examples/4/in.txt 

test4: compile4
	diff output.txt examples/4/implicit.first.txt

compile5:
	python3 hsim.py --free-list=implicit --fit=first examples/5/in.txt 

test5: compile5
	diff output.txt examples/5/implicit.first.txt

compile6:
	python3 hsim.py --free-list=implicit --fit=first examples/6/in.txt 

test6:compile6
	diff output.txt examples/6/implicit.first.txt

compile7:
	python3 hsim.py --free-list=implicit --fit=first examples/7/in.txt 

test7:compile7
	diff output.txt examples/7/implicit.first.txt

compile8:
	python3 hsim.py --free-list=implicit --fit=first examples/8/in.txt 

test8: compile8
	diff output.txt examples/8/implicit.first.txt

compile10:
	python3 hsim.py --free-list=implicit --fit=first examples/10/in.txt 

test10:compile10
	diff output.txt examples/10/implicit.first.txt

compile11:
	python3 hsim.py --free-list=implicit --fit=first examples/11/in.txt 

test11:compile11
	diff output.txt examples/11/implicit.first.txt

compile12:
	python3 hsim.py --free-list=implicit --fit=first examples/12/in.txt 

test12:compile12
	diff output.txt examples/12/implicit.first.txt

compile13:
	python3 hsim.py --free-list=implicit --fit=first examples/13/in.txt 

test13:compile13
	diff output.txt examples/13/implicit.first.txt