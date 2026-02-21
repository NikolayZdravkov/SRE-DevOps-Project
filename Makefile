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