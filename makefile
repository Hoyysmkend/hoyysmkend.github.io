# to build hugo pages

all_targe:all

all:build

build:
	@if [ -d "public/" ]; then \
		rm -r public/; \
		echo "remove public!!!"; \
		hugo; \
	else \
		hugo; \
	fi

.PNOYH:all_targe all build
