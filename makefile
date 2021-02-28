run:
	py nyancode.py

run-sample1:
	py nyancode.py samples/sample1.ncp

run-sample2:
	py nyancode.py samples/sample2.ncp

setup:
	py -m pip install -r requirements.txt
	cp github_hooks/pre-commit ./.git/hooks

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
