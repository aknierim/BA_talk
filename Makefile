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
TIKZ_PDFS := $(subst tikz/,,$(TIKZFILES:.tex=.pdf)) # get names from TikZ files for .pdf output files
TIKZ := $(addprefix build/tikz/,$(TIKZ_PDFS)) # add build/ to TikZ output files

# plots
cosmic_flux=build/cosmic_flux.pgf
crab_ssc=build/crab_ssc.pdf
array_layout=build/array_layout.pgf
fermi4fgl=build/fermi_catalog.pdf
ar_eff=build/AR_Aeff_MST_0.10_0.15.pdf build/AR_Aeff_MST_0.15_0.20.pdf build/AR_Aeff_MST_0.20_0.25.pdf \
	build/AR_Aeff_MST_0.25_0.30.pdf build/AR_Aeff_MST_0.30_0.35.pdf build/AR_Aeff_MST_0.35_0.40.pdf \
	build/AR_Aeff_MST_0.40_0.45.pdf
ar_vs_eff=build/ar_vs_eff.pdf
quantiles=build/quantiles_plot.pdf
metrics=build/metrics_tailcuts.pdf build/metrics_mars.pdf build/metrics_fact.pdf build/metrics_tcc.pdf \
	build/metrics_all.pdf
baseline=build/metrics_baseline.pdf build/Rel_AR_0.10_0.15_base.pdf build/Rel_AR_0.15_0.20_base.pdf \
	build/Rel_AR_0.20_0.25_base.pdf	build/Rel_AR_0.25_0.30_base.pdf build/Rel_AR_0.30_0.35_base.pdf \
	build/Rel_AR_0.35_0.40_base.pdf build/Rel_AR_0.40_0.45_base.pdf

# tables
tab_writer=build/tables.txt


PLOTS := $(ar_eff) $(ar_vs_eff) $(metrics) $(baseline) $(quantiles) # $(fermi4fgl)
TABLES := $(tab_writer)


# LaTeX options to disable interruptions
TeXOptions = -lualatex \
			 -interaction=nonstopmode \
			 -halt-on-error \
			 -output-directory=build

TikZOptions = -lualatex \
			  -interaction=nonstopmode \
			  -halt-on-error \
			  -output-directory=build/tikz


all: $(PLOTS) $(TIKZ) presentation_light.pdf presentation_dark.pdf

# plots
$(ar_eff): plots/angres_aeff.py matplotlibrc header-matplotlib.tex | build
	TEXINPUTS=$$(pwd): python -W ignore plots/angres_aeff.py --theme dark

$(ar_vs_eff): plots/ar_vs_eff.py matplotlibrc header-matplotlib.tex | build
	TEXINPUTS=$$(pwd): python plots/ar_vs_eff.py --theme dark

$(quantiles): plots/quantiles_plot.py matplotlibrc header-matplotlib.tex | build
	TEXINPUTS=$$(pwd): python plots/quantiles_plot.py --theme dark

$(metrics): plots/metrics.py matplotlibrc header-matplotlib.tex | build
	TEXINPUTS=$$(pwd): python plots/metrics.py --theme dark

$(baseline): plots/baseline.py matplotlibrc header-matplotlib.tex | build
	TEXINPUTS=$$(pwd): python -W ignore plots/baseline.py --theme dark

# $(fermi4fgl): plots/fermi_catalog.py matplotlibrc | build
# 	python plots/fermi_catalog.py

# tables
$(tab_writer): thesis_scripts/table_writer.py | build
	python thesis_scripts/table_writer.py

light: $(TIKZ) presentation_light.pdf

dark: $(TIKZ) presentation_dark.pdf

.DELETE_ON_ERROR:
presentation_light.pdf: FORCE | build
	@echo 0 > build/darktheme.var
	@TEXINPUTS=$$(pwd): latexmk $(TeXOptions) presentation.tex 1> build/log || cat build/log
	mv build/presentation.pdf $@

presentation_dark.pdf: FORCE | build
	@echo 1 > build/darktheme.var
	@TEXINPUTS=$$(pwd): latexmk $(TeXOptions) presentation.tex 1> build/log || cat build/log
	mv build/presentation.pdf $@

$(TIKZ): $(TIKZFILES) | build/tikz
	@echo "Compiling TikZ file $(BLUE)$(basename $(notdir $@)).tex$(RESET)"
	@TEXINPUTS=$$(pwd): latexmk $(TikZOptions) $(TIKZFILES) 1> \
		build/tikz/$(basename $(notdir $@))_log || cat build/tikz/$(basename $(notdir $@))_log


FORCE:

build:
	mkdir -p build/

build/tikz:
	mkdir -p build/tikz/

clean:
	@rm -rf build
	@echo ${GREEN}${BOLD}Removing build folder${RESET}

# remove LaTeX auxiliary files from build/
clean_tex:
	@rm -rf build/*.aux build/*.log build/*.out build/*.toc build/*.bbl build/*.blg build/*.fdb_latexmk build/*.fls build/*.synctex.gz
	@echo ${GREEN}${BOLD}Removing LaTeX auxiliary files${RESET}


.PHONY: FORCE all clean
