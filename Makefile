.PHONY: setup run check format docker-build docker-up docker-down logs clean

setup:
	@echo "Install dependencies"
	pip install -r requirements.txt

run:
	@echo "Run project locally"
	python app.py

check:
	@echo "Run linters"
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=120 --statistics

format:
	@echo "Format code"
	black .

docker-build:
	docker compose build

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down

logs:
	docker compose logs -f

clean:
	@echo "Clean up cache"
	find . -type d -name "__pycache__" -exec rm -rf {} +