init:
	pip install -r requirements.txt

test:
	python -m unittest 'tests/test_main.py' -v

coverage:
	coverage erase
	coverage run -a -m unittest 'tests/test_main.py'
	coverage html

pre:
	coverage run -a -m unittest 'tests/test_main.py'
	coverage html

flake8:
	flake8 pyCTelebot
    
po:
	xgettext --language=Python --output=pyCTelebot/locale/messages.pot pyCTelebot/pyCTelebotBase.py
	msgmerge --update --no-fuzzy-matching --backup=off pyCTelebot/locale/en/LC_MESSAGES/pyCTelebot.po pyCTelebot/locale/messages.pot
	msgmerge --update --no-fuzzy-matching --backup=off pyCTelebot/locale/es/LC_MESSAGES/pyCTelebot.po pyCTelebot/locale/messages.pot

mo:
	msgfmt pyCTelebot/locale/en/LC_MESSAGES/pyCTelebot.po -o pyCTelebot/locale/en/LC_MESSAGES/pyCTelebot.mo
	msgfmt pyCTelebot/locale/es/LC_MESSAGES/pyCTelebot.po -o pyCTelebot/locale/es/LC_MESSAGES/pyCTelebot.mo

pypi:
	python setup.py clean --all
	python setup.py sdist bdist_wheel
	twine upload dist/*
