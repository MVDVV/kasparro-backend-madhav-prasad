

up:
	docker-compose up --build

down:
	docker-compose down -v

logs:
	docker-compose logs -f


.PHONY: test

test:
	docker-compose exec app python -m pytest -q ./tests
