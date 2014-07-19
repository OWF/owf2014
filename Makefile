.PHONY: all

SRC=website

test:
	nosetests tests

run:
	./manage.py serve

index:
	rm -f whoosh_index/*
	./manage.py index_content

all:
	./manage.py build

clean:
	rm -rf data/abilian.db
	rm -rf build 
	rm -rf ./static/.webassets-cache
	rm -rf *.egg *.egg-info
	find . -name "*.pyc" | xargs rm -f
	find . -name packed.js | xargs rm -f
	find . -name packed.css | xargs rm -f

deploy:
	ansible-playbook -i deployment/hosts -v deployment/server.yml

fetch-db:
	rsync -vz -e ssh root@openwf.nexen.net:/srv/owf2014/src/data/abilian.db data/abilian.db

update-pot:
	# _n => ngettext, _l => lazy_gettext
	pybabel extract -F etc/babel.cfg -k "_n:1,2" -k "_l"\
    -o $(SRC)/translations/messages.pot "${SRC}"
	pybabel update -i $(SRC)/translations/messages.pot \
    -d $(SRC)/translations
	pybabel compile -d $(SRC)/translations

