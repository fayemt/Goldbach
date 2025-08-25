PDF=main
all: pdf

pdf:
	latexmk -pdf -interaction=nonstopmode $(PDF).tex

clean:
	latexmk -C

.PHONY: all pdf clean
