
.PHONY: help env up stop rm rmv rmi logs sh init_linters lint sqlmake sqlupgrade test dropmain updmain rsmain gha_ci_build_test_image _rm_test_container gha_ci_check_linting gha_ci_test gha_cd_updmain

# --- Application settings
default_env_file_name := .env
env_clone_dir := env_gist_temp

# --- Application virtual environment settings (can be changed)
env_file_name := .env
env_snippet_repo := git@github.com:ba2cdbc59e955b924f11ffc7a1c97530.git

# --- Docker
compose_cmd := docker compose -f
compose_local := $(compose_cmd) docker-compose-local.yml
compose_deployment := $(compose_cmd) docker-compose-deployment.yml
main_app_service_name := api

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
	@echo "    dropmain                 Stop and remove main app docker container with image and volume"
	@echo "    updmain                  Stop and remove old main app container with image and volume, rebuild and run new one"
	@echo "    rsmain                   Restart main app container"
	@echo "    logs                     Stdout logs from docker containers"
	@echo "    lint                     Run linting"
	@echo "    sqlmake MESSAGE          Make migrations with provided MESSAGE for the SQL database"
	@echo "    sqlrun                   Run migrations in the SQL database"
	@echo "    test                     Run tests for the API service"
	@echo "    gha_ci_build_test_image  Build test image into GitHub actions"
	@echo "    gha_ci_check_linting     Check linting for CI into GitHub actions"
	@echo "    gha_ci_test              Run tests for CI into GitHub actions"
	@echo "    gha_cd_updmain           Stop and remove old main app container with image and volume, rebuild and run new one for CD into GitHub actions"

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
	@$(compose_local) $(env_arg) up -d

stop: env
	@$(compose_local) $(env_arg) stop

rm: env
	@$(compose_local) $(env_arg) down

rmv: env
	@$(compose_local) $(env_arg) down -v

rmi: env
	@$(compose_local) $(env_arg) down --rmi all -v

logs: up
	@$(compose_local) logs -f

sh: up
	@docker exec -it $(firstword $(filter-out $@,$(MAKEOVERRIDES) $(MAKECMDGOALS))) sh

lint: init_linters
	@pre-commit run -a

sqlmake: up
	@docker exec -it pocket_assistant_api alembic revision --autogenerate -m $(addsuffix ",$(addprefix ",$(firstword $(filter-out $@,$(MAKEOVERRIDES) $(MAKECMDGOALS)))))

sqlupgrade: up
	@docker exec -it pocket_assistant_api alembic upgrade head

_rm_test_container:
	@docker rm $(test_api_container_name) -f

test: env
	@docker build -t $(test_api_image_name) .
	@docker run $(env_arg) --name $(test_api_container_name) $(test_api_image_name) pytest || true
	$(MAKE) _rm_test_container
	@docker rmi $(test_api_image_name)


gha_ci_build_test_image:
	@if [ -z $$(docker images -q $(test_api_image_name)) ]; then \
        docker build -t $(test_api_image_name) . ; \
    fi

gha_ci_check_linting: gha_ci_build_test_image
	@docker run $(env_arg) --name $(test_api_container_name) $(test_api_image_name) sh -c "autoflake . --check && black . --check && isort . --check && flake8"
	$(MAKE) _rm_test_container

gha_ci_test: gha_ci_build_test_image
	@docker run $(env_arg) --name $(test_api_container_name) $(test_api_image_name) pytest
	$(MAKE) _rm_test_container

gha_cd_updmain:
	@$(compose_deployment) $(env_arg) up -d --build $(main_app_service_name)

dropmain: env
	@$(compose_local) $(env_arg) down --rmi all -v $(main_app_service_name)

updmain: env
	@$(compose_local) $(env_arg) up -d --build $(main_app_service_name)

rsmain: env
	@$(compose_local) $(env_arg) restart $(main_app_service_name)