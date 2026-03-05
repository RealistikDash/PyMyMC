#!/usr/bin/make -f

install:
	python3 -m pip install -e .

run:
	python3 -m pymymc

build:
	python3 -m nuitka \
		--mode=app \
		--enable-plugin=pyqt5 \
		--include-data-dir=pymymc/resources=resources \
		--output-dir=dist \
		pymymc

clean:
	rm -rf dist/*.build dist/*.dist dist/*.onefile-build
