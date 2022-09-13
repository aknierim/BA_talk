#!/bin/bash
pwd := $$(pwd)

# colors / text formatting
BACKGR=`tput setaf 0`
RED=`tput setaf 1`
GREEN=`tput setaf 10`
GREENB=`tput setab 10`
BLUE=`tput setaf 4`
BOLD=`tput bold`
RESET=`tput sgr0`

# TikZ
TIKZFILES := $(wildcard tikz/*.tex) # list of all TikZ files
TIKZ_PDFS := $(subst tikz/,,$(TIKZFILES:.tex=)) # get names from TikZ files for .pdf output files

# plots
cosmic_flux=build/cosmic_flux.pgf
crab_ssc=build/crab_ssc.pdf
array_layout=build/array_layout.pgf
fermi4fgl=build/fermi_catalog.pdf
ar_eff=plots/ar_eff.pdf
ar_vs_eff=build/ar_vs_eff.pdf
quantiles=build/quantiles_plot.pdf
metrics=build/metrics.pdf
baseline=build/baseline.pdf

# tables
tab_writer=build/tables.txt


PLOTS := $(ar_eff) $(ar_vs_eff) $(metrics) $(baseline) $(quantiles) # $(fermi4fgl)
TABLES := $(tab_writer)


# LaTeX options to disable interruptions
TeXOptions = -lualatex \
			 -interaction=nonstopmode \
			 -halt-on-error \
			 -output-directory=build

# plots
$(ar_eff): plots/angres_aeff.py matplotlibrc | build
	python -W ignore plots/angres_aeff.py --theme dark

$(ar_vs_eff): plots/ar_vs_eff.py matplotlibrc | build
	python plots/ar_vs_eff.py --theme dark

$(quantiles): plots/quantiles_plot.py matplotlibrc | build
	python plots/quantiles_plot.py --theme dark

$(metrics): plots/metrics.py matplotlibrc | build
	python plots/metrics.py --theme dark

$(baseline): plots/baseline.py matplotlibrc | build
	python -W ignore plots/baseline.py --theme dark

# $(fermi4fgl): plots/fermi_catalog.py matplotlibrc | build
# 	python plots/fermi_catalog.py

# tables
$(tab_writer): thesis_scripts/table_writer.py | build
	python thesis_scripts/table_writer.py



all: $(PLOTS) presentation_light.pdf presentation_dark.pdf

light: presentation_light.pdf

dark: presentation_dark.pdf

.DELETE_ON_ERROR:
presentation_light.pdf: FORCE | build
	@echo 0 > build/darktheme.var
	@TEXINPUTS="$$(pwd):" latexmk $(TeXOptions) presentation.tex 1> build/log || cat build/log
	mv build/presentation.pdf $@

presentation_dark.pdf: FORCE | build
	@echo 1 > build/darktheme.var
	@TEXINPUTS="$$(pwd):" latexmk $(TeXOptions) presentation.tex 1> build/log || cat build/log
	mv build/presentation.pdf $@

tikz: FORCE tikz/ | build
	@TEXINPUTS="$$(pwd):" latexmk $(TeXOptions) $(TIKZFILES) 1> build/tikz_log || cat build/tikz_log
	@for name in $(TIKZ_PDFS) ; do \
		mv build/$$name.pdf graphics/$$name.pdf ; \
		rm build/$$name.aux build/$$name.fdb_latexmk build/$$name.fls build/$$name.log; \
	done


FORCE:

build:
	@mkdir -p build/

# simple workaround, else 'all' wouldn't work after 'presentation_light.pdf'
# (for whatever reason)
log:
	@mkdir -p build
	@touch build/log

clean:
	@rm -rf build
	@echo ${GREEN}${BOLD}Removing build folder${RESET}


.PHONY: all clean
