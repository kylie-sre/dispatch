install:
	python3 -m venv ~/.venv/dispatch
	DISPATCH_LIGHT_BUILD=1 ~/.venv/dispatch/bin/pip install -e .[dev]
	~/.venv/dispatch/bin/pip install ipdb

dev:
	~/.venv/dispatch/bin/dispatch server develop

serve:
	~/.venv/dispatch/bin/dispatch server start dispatch.main:app

initdb:
	~/.venv/dispatch/bin/dispatch database init

restore:
	~/.venv/dispatch/bin/dispatch database restore --dump-file ./data/dispatch-sample-data.dump

revision:
	~/.venv/dispatch/bin/dispatch database revision
