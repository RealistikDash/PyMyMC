#!/usr/bin/make -f

install:
	uv sync

run:
	uv run python -m pymymc

build:
	uv sync --extra build
	uv run python -m nuitka \
		--mode=app \
		--enable-plugin=pyside6 \
		--include-data-dir=pymymc/resources=resources \
		--include-package-data=minecraft_launcher_lib \
		--output-dir=dist \
		pymymc

lint:
	uvx pre-commit run --all-files

clean:
	rm -rf dist/*.build dist/*.dist dist/*.onefile-build
