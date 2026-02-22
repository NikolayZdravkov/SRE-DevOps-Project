install:
	pip install -r requirements.txt

run:
	python run.py

test:
	pytest tests/ -v

docker-build:
	docker build -t student-api:1.0.0 .

docker-run:
	docker run -p 5000:5000 --env-file .env student-api:1.0.0

start-db:
	docker compose up -d db

migrate: start-db
	flask db upgrade

start-api: docker-build migrate
	docker-compose up api

lint:
	flake8 app/ --max-line-length=120
