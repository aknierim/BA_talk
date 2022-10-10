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
ar_eff=build/AR_Aeff_MST_0.10_0.15_dark.pdf build/AR_Aeff_MST_0.15_0.20_dark.pdf build/AR_Aeff_MST_0.20_0.25_dark.pdf \
	build/AR_Aeff_MST_0.25_0.30_dark.pdf build/AR_Aeff_MST_0.30_0.35_dark.pdf build/AR_Aeff_MST_0.35_0.40_dark.pdf \
	build/AR_Aeff_MST_0.40_0.45_dark.pdf build/AR_Aeff_MST_0.10_0.15_light.pdf build/AR_Aeff_MST_0.15_0.20_light.pdf \
	build/AR_Aeff_MST_0.20_0.25_light.pdf build/AR_Aeff_MST_0.25_0.30_light.pdf build/AR_Aeff_MST_0.30_0.35_light.pdf \
	build/AR_Aeff_MST_0.35_0.40_light.pdf build/AR_Aeff_MST_0.40_0.45_light.pdf
ar_vs_eff=build/ar_vs_eff_dark.pdf build/ar_vs_eff_light.pdf
quantiles=build/quantiles_plot_dark.pdf build/quantiles_plot_light.pdf
metrics=build/metrics_tailcuts_dark.pdf build/metrics_mars_dark.pdf build/metrics_fact_dark.pdf build/metrics_tcc_dark.pdf \
	build/metrics_all_dark.pdf build/metrics_tailcuts_light.pdf build/metrics_mars_light.pdf build/metrics_fact_light.pdf \
	build/metrics_tcc_light.pdf build/metrics_all_light.pdf
baseline=build/metrics_baseline_dark.pdf build/Rel_AR_0.10_0.15_base_dark.pdf build/Rel_AR_0.15_0.20_base_dark.pdf \
	build/Rel_AR_0.20_0.25_base_dark.pdf build/Rel_AR_0.25_0.30_base_dark.pdf build/Rel_AR_0.30_0.35_base_dark.pdf \
	build/Rel_AR_0.35_0.40_base_dark.pdf build/Rel_AR_0.40_0.45_base_dark.pdf build/metrics_baseline_light.pdf \
	build/Rel_AR_0.10_0.15_base_light.pdf build/Rel_AR_0.15_0.20_base_light.pdf build/Rel_AR_0.20_0.25_base_light.pdf \
	build/Rel_AR_0.25_0.30_base_light.pdf build/Rel_AR_0.30_0.35_base_light.pdf build/Rel_AR_0.35_0.40_base_light.pdf \
	build/Rel_AR_0.40_0.45_base_light.pdf

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
