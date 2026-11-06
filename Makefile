IMAGE ?= omni-brain-mock:dev
PY ?= python3

.PHONY: install run test docker-build docker-run reset

install:
	$(PY) -m pip install -r requirements-dev.txt

run:
	$(PY) -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

test:
	$(PY) -m pytest -q

docker-build:
	docker build -t $(IMAGE) .

docker-run: docker-build
	docker run --rm -p 8080:8080 $(IMAGE)

reset:
	curl -s -X POST http://localhost:8080/admin/reset
