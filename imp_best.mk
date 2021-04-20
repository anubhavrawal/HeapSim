all: test1 test2 test3 test4 test5 test6 test7 test8 test9 test10 test11 test12 test13

compile1:
	python3 main.py --free-list=implicit --fit=best examples/examples/1/in.txt > 1.out

test1: compile1
	diff 1.out examples/examples/1/implicit.best.txt

compile2:
	python3 main.py --free-list=implicit --fit=best examples/examples/2/in.txt > 1.out

test2: compile2
	diff 1.out examples/examples/2/implicit.best.txt

compile3:
	python3 main.py --free-list=implicit --fit=best examples/examples/3/in.txt > 1.out

test3:compile3
	diff 1.out examples/examples/3/implicit.best.txt

compile4:
	python3 main.py --free-list=implicit --fit=best examples/examples/4/in.txt > 1.out

test4: compile4
	diff 1.out examples/examples/4/implicit.best.txt

compile5:
	python3 main.py --free-list=implicit --fit=best examples/examples/5/in.txt > 1.out

test5: compile5
	diff 1.out examples/examples/5/implicit.best.txt

compile6:
	python3 main.py --free-list=implicit --fit=best examples/examples/6/in.txt > 1.out

test6:compile6
	diff 1.out examples/examples/6/implicit.best.txt

compile7:
	python3 main.py --free-list=implicit --fit=best examples/examples/7/in.txt > 1.out

test7:compile7
	diff 1.out examples/examples/7/implicit.best.txt

compile8:
	python3 main.py --free-list=implicit --fit=best examples/examples/8/in.txt > 1.out

test8: compile8
	diff 1.out examples/examples/8/implicit.best.txt

compile9:
	python3 main.py --free-list=implicit --fit=best examples/examples/9/in.txt > 1.out

test9:compile9
	diff 1.out examples/examples/9/implicit.best.txt

compile10:
	python3 main.py --free-list=implicit --fit=best examples/examples/10/in.txt > 1.out

test10:compile10
	diff 1.out examples/examples/10/implicit.best.txt

compile11:
	python3 main.py --free-list=implicit --fit=best examples/examples/11/in.txt > 1.out

test11:compile11
	diff 1.out examples/examples/11/implicit.best.txt

compile12:
	python3 main.py --free-list=implicit --fit=best examples/examples/12/in.txt > 1.out

test12:compile12
	diff 1.out examples/examples/12/implicit.best.txt

compile13:
	python3 main.py --free-list=implicit --fit=best examples/examples/13/in.txt > 1.out

test13:compile13
	diff 1.out examples/examples/13/implicit.best.txt