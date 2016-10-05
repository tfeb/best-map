# This is just a bunch of shorthands
#

.PHONY: default install develop uninstall clean veryclean ready recent\
	test compare sanity

PYTHON  = python
PACKAGE = bestmap

default: ready

# ready & recent mean you can use garmr to watch things
#

ready:
	@git status

recent:
	@git --no-pager log -20 --format="%h / %an / %ar / %s%d"

# clean just nukes compiled things and should be safe, veryclean
# cleans up backups which might not be.
#

clean:
	find . -type f -name '*.pyc' -print0 | xargs -0 -r rm

veryclean: clean
	find . -type f -name '*~' -print0 | xargs -0 -r rm
	$(PYTHON) setup.py clean
	rm -rf build

# The tests are slow enough and there are few enough of them it is
# useful to see them
#
test: clean
	nosetests -v

# clean and test before installing, just clean before installing for
# development
#

install: clean test
	$(PYTHON) setup.py install

develop: clean
	$(PYTHON) setup.py develop

uninstall:
	pip uninstall -y $(PACKAGE)
