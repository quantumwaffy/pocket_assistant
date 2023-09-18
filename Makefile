.PHONY: help env up stop rm rmv rmi logs sh init_linters lint sqlmake sqlupgrade test check_lint

# --- Application settings
default_env_file_name := .env
env_clone_dir := env_gist_temp

# --- Application virtual environment settings (can be changed)
env_file_name := .env
env_snippet_repo := git@github.com:ba2cdbc59e955b924f11ffc7a1c97530.git

# --- Docker
compose := docker compose -f docker-compose-local.yml
env_arg := --env-file .env
dockerfile_name := Dockerfile.local

# --- Docker test
test_api_container_name := pocket_assistant_test_api
test_api_image_name := pocket_assistant_test_api_image


help:
	@echo "Please use 'make <target>' where <target> is one of:"
	@echo "    up                       Run docker containers"
	@echo "    stop                     Stop docker containers"
	@echo "    rm                       Stop and remove docker containers"
	@echo "    rmv                      Stop and remove docker containers with their volumes"
	@echo "    rmi                      Stop and remove docker containers with their images and volumes"
	@echo "    logs                     Stdout logs from docker containers"
	@echo "    lint                     Run linting"
	@echo "    sqlmake MESSAGE          Make migrations with provided MESSAGE for the SQL database"
	@echo "    sqlrun                   Run migrations in the SQL database"
	@echo "    test                     Run tests for the API service"

env:
	@if [ ! -f $(default_env_file_name) ]; then \
  		git clone  $(env_snippet_repo) $(env_clone_dir) && \
  		mv $(env_clone_dir)/$(env_file_name) ./$(default_env_file_name) && \
  		rm -rf $(env_clone_dir); \
  	fi
  	env_arg := --env-file $(default_env_file_name)

init_linters:
	@pre-commit install

up: env
	@$(compose) $(env_arg) up -d

stop: env
	@$(compose) $(env_arg) stop

rm: env
	@$(compose) $(env_arg) down

rmv: env
	@$(compose) $(env_arg) down -v

rmi: env
	@$(compose) $(env_arg) down --rmi all -v

logs: up
	@$(compose) logs -f

sh: up
	@docker exec -it $(firstword $(filter-out $@,$(MAKEOVERRIDES) $(MAKECMDGOALS))) sh

lint: init_linters
	@pre-commit run -a

sqlmake: up
	@docker exec -it pocket_assistant_api alembic revision --autogenerate -m $(addsuffix ",$(addprefix ",$(firstword $(filter-out $@,$(MAKEOVERRIDES) $(MAKECMDGOALS)))))

sqlupgrade: up
	@docker exec -it pocket_assistant_api alembic upgrade head

test: env
	@docker build -t $(test_api_image_name) -f $(dockerfile_name) .
	@docker run $(env_arg) --name $(test_api_container_name) $(test_api_image_name) pytest || true
	@docker rm $(test_api_container_name) -f
	@docker rmi $(test_api_image_name)

check_lint:
	@autoflake . --check
	@black . --check
	@isort . --check
	@flake8