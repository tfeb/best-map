# This is just a bunch of shorthands
#

.PHONY: default install develop uninstall clean veryclean ready recent\
	test compare sanity

MODULES	= best-map.rkt
RACO	= raco

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
	rm -rf compiled

veryclean: clean
	find . -type f -name '*~' -print0 | xargs -0 -r rm

test: clean
	$(RACO) test $(MODULES)
