# clockgr - A fullscreen clock for Qt
# Copyright (C) 2015 Ingo Ruhnke <grumbel@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

SOURCES := $(wildcard \
  *.py \
  clockgr_qt/*.py)

default: flake test pylint

all: autopep flake test pylint

autopep:
	autopep8 --max-line=120 --in-place --aggressive $(SOURCES)

test:
	python2 -m unittest discover -s tests/

flake:
	python2 -m flake8.run --max-line-length=120 $(SOURCES)

PYLINT_TARGETS := $(addprefix .pylint/, $(SOURCES))

$(PYLINT_TARGETS): .pylint/%.py: %.py
	mkdir -p $(dir $@)
	PYTHONPATH=. epylint3 $< --rcfile=.pylintrc --max-line-length=120 --extension-pkg-whitelist=PyQt5
	touch $@

pylint: $(PYLINT_TARGETS)

clean:
	rm -vrf .pylint/

run:
	python3 -m clockgr_qt

.PHONY: autopep test flake pylint clean all default run

# EOF #
