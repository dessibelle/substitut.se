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

DJANGO_SETTINGS_MODULE = $(PROJECT).settings
DJANGO_POSTFIX = --settings=$(DJANGO_SETTINGS_MODULE) --pythonpath=$(PYTHONPATH)
DJANGO_LOCAL_SETTINGS_MODULE = $(PROJECT).settings
DJANGO_LOCAL_POSTFIX = --settings=$(DJANGO_LOCAL_SETTINGS_MODULE) --pythonpath=$(PYTHONPATH)
DJANGO_TEST_SETTINGS_MODULE = $(PROJECT).settings
DJANGO_POSTFIX = --settings=$(DJANGO_SETTINGS_MODULE) --pythonpath=$(PYTHONPATH)
DJANGO_TEST_POSTFIX = --settings=$(DJANGO_TEST_SETTINGS_MODULE) --pythonpath=$(PYTHONPATH)
PYTHON_BIN = $(VIRTUAL_ENV)/bin

# JS files to be compressed
COMPRESS = "$(STATICPATH)/recipes/js/vote.js" \
	"$(STATICPATH)/recipes/js/exceptions.js" \
	"$(STATICPATH)/recipes/js/storage.js" \
	"$(STATICPATH)/recipes/js/recipe.js" \
	"$(STATICPATH)/recipes/js/substitut.js" \
	"$(STATICPATH)/recipes/js/templates/templates.js"

COMBINE_COMPRESSED = "lib/jquery/dist/jquery.min.js" \
	"lib/jquery-ui/jquery-ui.min.js" \
	"lib/jquery-unveil/jquery.unveil.min.js" \
	"lib/handlebars/handlebars.runtime.js" \
	"lib/parallax/parallax.min.js" \
	"recipes/js/final/substitut.min.js"

COMBINE_ALL = "$(STATICPATH)/lib/jquery/dist/jquery.js" \
	"$(STATICPATH)/lib/jquery-ui/jquery-ui.js" \
	"$(STATICPATH)/lib/jquery-unveil/jquery.unveil.js" \
	"$(STATICPATH)/lib/handlebars/handlebars.runtime.js" \
	"$(STATICPATH)/lib/parallax/parallax.js" \
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

showenv:
	@echo 'Environment:'
	@echo '-----------------------'
	@$(PYTHON_BIN)/python -c "import sys; print 'sys.path:', sys.path"
	@echo 'PYTHONPATH:' $(PYTHONPATH)
	@echo 'PROJECT:' $(PROJECT)
	@echo 'DJANGO_SETTINGS_MODULE:' $(DJANGO_SETTINGS_MODULE)
	@echo 'DJANGO_LOCAL_SETTINGS_MODULE:' $(DJANGO_LOCAL_SETTINGS_MODULE)
	@echo 'DJANGO_TEST_SETTINGS_MODULE:' $(DJANGO_TEST_SETTINGS_MODULE)

showenv.all: showenv showenv.virtualenv showenv.site

showenv.virtualenv: virtual_env_set
	PATH := $(VIRTUAL_ENV)/bin:$(PATH)
	export $(PATH)
	@echo 'VIRTUAL_ENV:' $(VIRTUAL_ENV)
	@echo 'PATH:' $(PATH)

showenv.site: site_set
	@echo 'SITE:' $(SITE)

djangohelp: virtual_env_set
	$(PYTHON_BIN)/django-admin.py help $(DJANGO_POSTFIX)

collectstatic: virtual_env_set
	-mkdir -p .$(LOCALPATH)/static
	$(PYTHON_BIN)/django-admin.py collectstatic -c --noinput $(DJANGO_POSTFIX)

runserver: virtual_env_set
	$(PYTHON_BIN)/django-admin.py runserver $(DJANGO_POSTFIX)

syncdb: virtual_env_set
	$(PYTHON_BIN)/django-admin.py syncdb $(DJANGO_POSTFIX)

cmd: virtual_env_set
	$(PYTHON_BIN)/django-admin.py $(CMD) $(DJANGO_POSTFIX)

localcmd: virtual_env_set
	$(PYTHON_BIN)/django-admin.py $(CMD) $(DJANGO_LOCAL_POSTFIX)

refresh:
	touch src/$(PROJECT)/*wsgi.py

rsync:
	rsync -avz --checksum --exclude-from .gitignore --exclude-from .rsyncignore . $(REMOTE_URI)

compare:
	rsync -avz --checksum --dry-run --exclude-from .gitignore --exclude-from .rsyncignore . $(REMOTE_URI)

clean:
	find . -name "*.pyc" -print0 | xargs -0 rm -rf
	-rm -rf htmlcov
	-rm -rf .coverage
	-rm -rf build
	-rm -rf dist
	-rm -rf src/*.egg-info

test: clean virtual_env_set
	-$(PYTHON_BIN)/coverage run $(PYTHON_BIN)/django-admin.py test $(APP) $(DJANGO_TEST_POSTFIX)

coverage: virtual_env_set
	$(PYTHON_BIN)/coverage html --include="$(LOCALPATH)/*" --omit="*/admin.py,*/test*"

predeploy: test

register: virtual_env_set
	python setup.py register

sdist: virtual_env_set
	python setup.py sdist

upload: sdist virtual_env_set
	python setup.py upload
	make clean

bootstrap: virtualenv pip virtual_env_set

pip: requirements/$(SETTINGS).txt virtual_env_set
	pip install -r requirements/$(SETTINGS).txt

virtualenv:
	virtualenv --no-site-packages $(VIRTUAL_ENV)
	echo $(VIRTUAL_ENV)

all: collectstatic refresh
