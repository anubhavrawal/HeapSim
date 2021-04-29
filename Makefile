run: hsim.py Heap.py in.txt
	python3 hsim.py --free-list=implicit --fit=best in.txt

clean:
	rm -f output.txt