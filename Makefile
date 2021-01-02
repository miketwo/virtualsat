.PHONY: init
init:
	pip install -r requirements.txt

.PHONY: test
test:
	find . -name \*.pyc -delete
	ptw --poll -- --verbose --capture=no --cache-clear
