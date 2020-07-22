install:
	python3 -m venv ~/.venv/dispatch
	DISPATCH_LIGHT_BUILD=1 ~/.venv/dispatch/bin/pip install -e .[dev]
	~/.venv/dispatch/bin/pip install ipdb

freeze:
	@~/.venv/dispatch/bin/pip freeze

dev:
	~/.venv/dispatch/bin/dispatch server develop

serve:
	~/.venv/dispatch/bin/dispatch server start dispatch.main:app

initdb:
	docker-compose up -d postgres
	~/.venv/dispatch/bin/dispatch database init
	docker-compose stop

restore:
	docker-compose up -d postgres
	~/.venv/dispatch/bin/dispatch database restore --dump-file ./data/dispatch-sample-data.dump
	docker-compose stop

revision:
	~/.venv/dispatch/bin/dispatch database revision

base:
	docker build -t gcr.io/unity-ie-sre-isolated-test/dispatch:base -f Dockerfile.base .

image:
	docker build -t gcr.io/unity-ie-sre-isolated-test/dispatch:server .
