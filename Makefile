SOURCES := $(wildcard \
  clockgr/*.py \
  clockgr/desklets/*.py)

all: autopep flake test

autopep:
	autopep8  --max-line=120  --in-place $(SOURCES)

test:
	python2 -m unittest discover -s tests/

flake:
	python2 -m flake8.run --max-line-length=120 $(SOURCES)

PYLINT_TARGETS := $(addprefix .pylint/, $(SOURCES))

$(PYLINT_TARGETS): .pylint/%.py: %.py
	mkdir -p $(dir $@)
	PYTHONPATH=. epylint $<
	touch $@

pylint: $(PYLINT_TARGETS)

clean:
	rm -vrf .pylint/

.PHONY: autopep test flake pylint clean

# EOF #
