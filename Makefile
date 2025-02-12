DC = docker compose
EXEC = docker exec -it
APP_FILE = docker_compose/app.yaml
STORAGES_FILE = docker_compose/storage.yaml
DB_CONTAINER = financial_diary_db
ENV_FILE = --env-file ../DimaTechTest/.env_docker
APP_CONTAINER = financial_diary_back
LOGS = docker logs

.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV_FILE} up -d

.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} down

.PHONY: postgres
postgres:
	${EXEC} ${DB_CONTAINER} psql -U postgres -d financial_diary

.PHONY: storages-logs
storages-logs:
	${LOGS} ${DB_CONTAINER} -f

.PHONY: app
app:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} ${ENV_FILE} up -d --force-recreate --build

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} down

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f