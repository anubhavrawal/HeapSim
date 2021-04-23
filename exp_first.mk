all: test1 test2 test3 test4 test5 test6 test7 test8 test9 test10 test11 test12 test13

compile1:
	python3 main.py --free-list=explicit --fit=first examples/examples/1/in.txt 

test1: compile1
	diff output.txt examples/examples/1/explicit.first.txt

compile2:
	python3 main.py --free-list=explicit --fit=first examples/examples/2/in.txt 

test2: compile2
	diff output.txt examples/examples/2/explicit.first.txt

compile3:
	python3 main.py --free-list=explicit --fit=first examples/examples/3/in.txt 

test3:compile3
	diff output.txt examples/examples/3/explicit.first.txt

compile4:
	python3 main.py --free-list=explicit --fit=first examples/examples/4/in.txt 

test4: compile4
	diff output.txt examples/examples/4/explicit.first.txt

compile5:
	python3 main.py --free-list=explicit --fit=first examples/examples/5/in.txt 

test5: compile5
	diff output.txt examples/examples/5/explicit.first.txt

compile6:
	python3 main.py --free-list=explicit --fit=first examples/examples/6/in.txt 

test6:compile6
	diff output.txt examples/examples/6/explicit.first.txt

compile7:
	python3 main.py --free-list=explicit --fit=first examples/examples/7/in.txt 

test7:compile7
	diff output.txt examples/examples/7/explicit.first.txt

compile8:
	python3 main.py --free-list=explicit --fit=first examples/examples/8/in.txt 

test8: compile8
	diff output.txt examples/examples/8/explicit.first.txt

compile10:
	python3 main.py --free-list=explicit --fit=first examples/examples/10/in.txt 

test10:compile10
	diff output.txt examples/examples/10/explicit.first.txt

compile11:
	python3 main.py --free-list=explicit --fit=first examples/examples/11/in.txt 

test11:compile11
	diff output.txt examples/examples/11/explicit.first.txt

compile12:
	python3 main.py --free-list=explicit --fit=first examples/examples/12/in.txt 

test12:compile12
	diff output.txt examples/examples/12/explicit.first.txt

compile13:
	python3 main.py --free-list=explicit --fit=first examples/examples/13/in.txt 

test13:compile13
	diff output.txt examples/examples/13/explicit.first.txt