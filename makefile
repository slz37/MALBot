.PHONY : build test run clean

build :
	@chmod -R *
	
run :
	@python main.py
	
test :
	@python test.py

clean :
	@rm -rf __pycache__
	@rm -rf pckg/src/__pycache__
	@rm -rf pckg/tests/__pycache__
	@rm -rf debug
	@rm -rf *.pyc