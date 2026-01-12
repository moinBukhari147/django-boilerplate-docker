SHELL=/bin/bash

dc := docker compose

success := success

build:
	@$(dc) build

up:
	@$(dc) up -d
	@echo "$(success)"

down:
	@$(dc) down --remove-orphans
	@echo "$(success)"

downv:
	@$(dc) down --remove-orphans -v

restart:
	@$(dc) restart
	@echo "$(success)"

logs:
	@$(dc) logs -f

djangologs:
	@$(dc) logs -f django

prune:
	@docker system prune -af --volumes

# ------------------------
# Django one-off commands
# ------------------------
dcshell:
	@$(dc) exec django /bin/bash

sp:
	@$(dc) exec django uv run python manage.py shell_plus

makemigrations:
	@$(dc) exec django uv run python manage.py makemigrations

migrate:
	@$(dc) exec django uv run python manage.py migrate

collectstatic:
	@$(dc) exec django uv run python manage.py collectstatic --noinput

createsuperuser:
	@$(dc) exec django uv run python manage.py createsuperuser

# ------------------------
# Celery commands
# ------------------------
celery-worker:
	@$(dc) exec celery celery -A config worker -l info

celery-beat:
	@$(dc) exec celery celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

flower:
	@$(dc) exec flower

# ------------------------
# Database & Redis
# ------------------------
psql:
	@$(dc) exec postgres psql -U postgres

rediscli:
	@$(dc) exec redis redis-cli -h redis

# ------------------------
# Tests
# ------------------------
test:
	@$(dc) up -d django
	@$(dc) exec -T django python manage.py migrate
	@$(dc) exec -T django python manage.py collectstatic --no-input
	@$(dc) exec -T django python -m coverage run --source='.' manage.py test --no-input
	@$(dc) exec -T django python -m coverage html -d htmlcov
	@$(dc) down --remove-orphans
