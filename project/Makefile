SHELL := /bin/sh

# Project settings
PROJECT := project

# Colors
CCRED := $(shell echo "\033[0;31m")
CCYELLOW := $(shell echo "\033[0;33m")
CCEND := $(shell echo "\033[0m")

# Common paths

THIS_FILE := $(lastword $(MAKEFILE_LIST))
PROJECTPATH:= $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

PYTHONPATH = $(PROJECTPATH)/
SASSPATH = $(PROJECTPATH)/sass
STATICPATH = $(PROJECTPATH)/static
SCRIPTPATH = $(PROJECTPATH)/scripts
JSPATH = $(STATICPATH)/recipes/js

# Final output css and js files
CSSFILE = $(STATICPATH)/recipes/css/substitut.css
COMPRESSEDFILE = $(STATICPATH)/recipes/js/final/substitut.min.js
HANDLEBARSFILE = $(STATICPATH)/recipes/js/templates/templates.js
JSMINFILE = $(STATICPATH)/recipes/js/final/app.min.js
JSFILE = $(STATICPATH)/recipes/js/final/app.js

LOCALPATH := ./project

DJANGO_SETTINGS_MODULE = $(PROJECT).settings.local
DJANGO_POSTFIX = --settings=$(DJANGO_SETTINGS_MODULE) --pythonpath=$(PYTHONPATH)
DJANGO_LOCAL_SETTINGS_MODULE = $(PROJECT).settings
DJANGO_LOCAL_POSTFIX = --settings=$(DJANGO_LOCAL_SETTINGS_MODULE) --pythonpath=$(PYTHONPATH)
DJANGO_TEST_SETTINGS_MODULE = $(PROJECT).settings
DJANGO_POSTFIX = --settings=$(DJANGO_SETTINGS_MODULE) --pythonpath=$(PYTHONPATH)
DJANGO_TEST_POSTFIX = --settings=$(DJANGO_TEST_SETTINGS_MODULE) --pythonpath=$(PYTHONPATH)
PYTHON_BIN = $(VIRTUAL_ENV)/bin

# JS files to be compressed
COMPRESS = "$(STATICPATH)/recipes/js/init.js" \
	"$(STATICPATH)/recipes/js/substitut.js" \
	"$(STATICPATH)/recipes/js/vote.js" \
	"$(STATICPATH)/recipes/js/exceptions.js" \
	"$(STATICPATH)/recipes/js/storage.js" \
	"$(STATICPATH)/recipes/js/recipe.js" \
	"$(STATICPATH)/recipes/js/responsive.js" \
	"$(STATICPATH)/recipes/js/templates/templates.js" \
	"$(STATICPATH)/recipes/js/main.js"

COMBINE_COMPRESSED = "lib/jquery/dist/jquery.min.js" \
	"lib/jquery-ui/jquery-ui.min.js" \
	"lib/hisrc/hisrc.js" \
	"lib/handlebars/handlebars.runtime.js" \
	"lib/parallax/parallax.min.js" \
	"lib/bootstrap/dist/js/bootstrap.min.js" \
	"recipes/js/final/substitut.min.js"

COMBINE_ALL = "$(STATICPATH)/lib/jquery/dist/jquery.js" \
	"$(STATICPATH)/lib/jquery-ui/jquery-ui.js" \
	"$(STATICPATH)/lib/hisrc/hisrc.js" \
	"$(STATICPATH)/lib/handlebars/handlebars.runtime.js" \
	"$(STATICPATH)/lib/parallax/parallax.js" \
	"$(STATICPATH)/lib/bootstrap/dist/js/bootstrap.js" \
	$(COMPRESS)

.PHONY: clean showenv coverage test bootstrap pip virtualenv sdist virtual_env_set

.PHONY: js
js: handlebars combine-all clean-handlebars
	@echo "$(CCYELLOW)Done!$(CCEND)"
	@echo ""

.PHONY: js-min
js-min: handlebars compress combine-compressed clean-compressed clean-handlebars
	@echo "$(CCYELLOW)Done!$(CCEND)"
	@echo ""

clean-css:
ifneq ($(wildcard $(CSSFILE)),)
	@echo "Deleting old file: $(CSSFILE)"
	@-rm -f $(CSSFILE)
endif

clean-handlebars:
ifneq ($(wildcard $(HANDLEBARSFILE)),)
	@echo "Deleting old file: $(HANDLEBARSFILE)"
	@-rm -f $(HANDLEBARSFILE)
endif

.PHONY: clean-css
css: clean-css
	@echo "$(CCYELLOW)Compiling css ...$(CCEND)"
	@scss $(SASSPATH)/app.scss > $(CSSFILE)
ifneq ($(wildcard $(CSSFILE)),)
	@echo "Created file: $(CSSFILE)";
	@echo "$(CCYELLOW)Done!$(CCEND)"
	@echo ""
else
	@echo "$(CCRED)Could not create file: $(CSSFILE)$(CCEND)"; \
	@echo ""
	exit 1;
endif

handlebars: clean-handlebars
	@echo "$(CCYELLOW)Compiling handlebars templates ...$(CCEND)"
	@handlebars $(STATICPATH)/recipes/js/templates/ > $(HANDLEBARSFILE)
ifneq ($(wildcard $(HANDLEBARSFILE)),)
	@echo "Created file: $(HANDLEBARSFILE)";
else
	@echo "$(CCRED)Could not create file: $(HANDLEBARSFILE)$(CCEND)"; \
	@echo ""
	exit 1;
endif

clean-js-min:
ifneq ($(wildcard $(JSMINFILE)),)
	@echo "Deleting old file: $(JSMINFILE)"
	@-rm -f $(JSMINFILE)
endif
	@touch $(JSMINFILE)

clean-js:
ifneq ($(wildcard $(JSFILE)),)
	@echo "Deleting old file: $(JSFILE)"
	@-rm -f $(JSFILE)
endif
	@touch $(JSFILE)

clean-compressed:
	@echo "Removing: $(COMPRESSEDFILE)"
	@-rm -f $(COMPRESSEDFILE)

.PHONY: combine-compressed
combine-compressed: clean-js-min $(COMBINE_COMPRESSED)
ifneq ($(wildcard $(JSMINFILE)),)
	@echo "Created file: $(JSMINFILE)";
else
	@echo "$(CCRED)Could not create file: $(JSMINFILE)$(CCEND)"; \
	@echo ""
	exit 1;
endif

.PHONY: combine-all
combine-all: clean-js $(COMBINE_ALL)
ifneq ($(wildcard $(JSFILE)),)
	@echo "Created file: $(JSFILE)";
else
	@echo "$(CCRED)Could not create file: $(JSFILE)$(CCEND)"; \
	@echo ""
	exit 1;
endif

$(COMBINE_COMPRESSED): $(JSMINFILE)
	@echo "Merge: $(STATICPATH)/$@"
	@cat $(STATICPATH)/$@ >> $(JSMINFILE)

$(COMBINE_ALL): $(JSFILE)
	@echo "Merge: $@"
	@cat $@ >> $(JSFILE)

.PHONY: index
index:
	@echo "$(CCYELLOW)Indexing ...$(CCEND)"
	@$(PYTHON_BIN)/django-admin.py index $(DJANGO_POSTFIX)
	@echo "$(CCYELLOW)Done!$(CCEND)"
	@echo ""

.PHONY: index-votes
index-votes:
	@echo "$(CCYELLOW)Indexing votes ...$(CCEND)"
	@$(PYTHON_BIN)/django-admin.py index_votes $(DJANGO_POSTFIX)
	@echo "$(CCYELLOW)Done!$(CCEND)"
	@echo ""

compress:
	@$(SCRIPTPATH)/compressjs.sh $(COMPRESS) $(COMPRESSEDFILE)