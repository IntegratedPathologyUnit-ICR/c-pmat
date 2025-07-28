# # Minimal makefile for Sphinx documentation
# #
#
# # You can set these variables from the command line, and also
# # from the environment for the first two.
# SPHINXOPTS    ?=
# SPHINXBUILD   ?= sphinx-build
# SOURCEDIR     = .
# BUILDDIR      = _build
#
# # Put it first so that "make" without argument is like "make help".
# help:
# 	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
#
# .PHONY: help Makefile
#
# # Catch-all target: route all unknown targets to Sphinx using the new
# # "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
# %: Makefile
# 	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD  ?= sphinx-build
SOURCEDIR    = .
BUILDDIR     = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile clean html livehtml

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Clean build directory
clean:
	rm -rf $(BUILDDIR)/*
	rm -rf api/_autosummary/

# Build HTML documentation
html:
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

# Build HTML and watch for changes (requires sphinx-autobuild)
livehtml:
	sphinx-autobuild "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)

# Build documentation and check for warnings
htmlstrict:
	@$(SPHINXBUILD) -W -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)

# Build LaTeX/PDF documentation
latexpdf:
	@$(SPHINXBUILD) -b latex "$(SOURCEDIR)" "$(BUILDDIR)/latex" $(SPHINXOPTS) $(O)
	@echo "Running LaTeX files through pdflatex..."
	$(MAKE) -C $(BUILDDIR)/latex all-pdf
	@echo "pdflatex finished; the PDF files are in $(BUILDDIR)/latex."

# Check documentation for broken links
linkcheck:
	@$(SPHINXBUILD) -b linkcheck "$(SOURCEDIR)" "$(BUILDDIR)/linkcheck" $(SPHINXOPTS) $(O)
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in $(BUILDDIR)/linkcheck/output.txt."

# Build documentation for different formats
epub:
	@$(SPHINXBUILD) -b epub "$(SOURCEDIR)" "$(BUILDDIR)/epub" $(SPHINXOPTS) $(O)
	@echo
	@echo "Build finished. The epub file is in $(BUILDDIR)/epub."

# Check spelling (requires sphinxcontrib-spelling)
spelling:
	@$(SPHINXBUILD) -b spelling "$(SOURCEDIR)" "$(BUILDDIR)/spelling" $(SPHINXOPTS) $(O)
	@echo
	@echo "Spell check complete; look for any errors in the above output " \
	      "or in $(BUILDDIR)/spelling/output.txt."

# Generate API documentation automatically
apidoc:
	sphinx-apidoc -o api/ ../ ../setup.py --separate --force
	@echo "API documentation generated in api/"

# Full clean build
fullclean:
	rm -rf $(BUILDDIR)
	rm -rf api/_autosummary/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +

# Install documentation dependencies
install-docs:
	pip install -r requirements-docs.txt

# Build and serve documentation locally
serve: html
	@echo "Starting local server at http://localhost:8000"
	@cd $(BUILDDIR)/html && python -m http.server 8000

# Build documentation for deployment
deploy: clean html
	@echo "Documentation built and ready for deployment from $(BUILDDIR)/html"

# Check documentation quality
quality: htmlstrict linkcheck spelling
	@echo "Documentation quality checks complete"

# Build all documentation formats
all: html epub latexpdf
	@echo "All documentation formats built"