run: main.py in.txt
	python3 main.py --free-list=implicit --fit=best in.txt

clean:
	rm -f output.txt