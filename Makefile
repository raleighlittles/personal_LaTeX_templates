# Makefile for cleaning targets in the LaTeX templates directory. 
# This will delete all .aux, .log, .bak, and .synctex.gz files in the current directory and all subdirectories.

.PHONY: clean
clean:
	find . -iname "*.aux" -delete -print
	find . -iname "*.log" -delete -print
	find . -iname "*.bak" -delete -print
	find . -iname "*.synctex.gz" -delete -print