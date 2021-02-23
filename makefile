run:
	py nyancode.py

fmt:
	py -m autopep8 -r -i -a -a .
test:
	py -m unittest discover tests
.PHONY: clear-keymap
clear-keymap:
	rm keymap.ini
.PHONY: bumpup
bumpup:
	py tools\bumpup.py
.PHONY: build
build:
	py tools\build.py
