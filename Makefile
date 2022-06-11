all: init

init: venv
	@make install

VENV_PATH=./venv/

venv:
	python3 -m venv $(VENV_PATH)

install: requirements.txt.lock

%.txt.lock: %.txt
	@( \
		source $(VENV_PATH)bin/activate; \
		pip3 install -r $<; \
		cat $< > $@ \
	)

requirements.txt.lock: requirements.txt

clean:
	rm -rf $(VENV_PATH)
	rm requirements.txt.lock
	rm db.sqlite3

run: init
	@( \
		source $(VENV_PATH)bin/activate; \
		python3 manage.py runserver \
	)

# $(make activate)
activate:
	@echo "source $(VENV_PATH)bin/activate"

.PHONY: all init install clean run activate
