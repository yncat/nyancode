run:
	py application.py

fmt:
	py -m autopep8 -r -i -a -a .
test:
	py -m unittest discover tests
clear-keymap:
	rm keymap.ini
