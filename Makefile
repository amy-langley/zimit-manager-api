.PHONY: clean count docker-build init lint start test

# annoying
export DOCKER_CLI_HINTS=false

clean:
	-rm *.db
	-rm -rf dist
	-find . -type d -name "*.egg-info" -exec rm -rf {} +
	-find . -type d -name "*cache*" -exec rm -rf {} +
	-docker rm `docker ps -a | grep hello-world | cut -d' ' -f1`
	-docker rmi hello-world
	-docker rmi ghcr.io/openzim/zimit

count:
	-wc -l `find src -name "*.py"`
	-wc -l `find tests -name "*.py"`
	-wc -l Makefile Dockerfile

docker-build:
	docker build . -t zimit-manager

docker-run: docker-build
	docker run											\
		-p 8000:8000									\
		-v ./var/data:/data								\
		-v ./var/output:/output							\
		-v /var/run/docker.sock:/var/run/docker.sock	\
		--name zimit-manager							\
		zimit-manager

docker-shell: docker-build
	docker run -it --entrypoint sh zimit-manager

init:
	pdm install -d
	pre-commit install

lint:
	isort .
	black .
	flake8 .

start:
	docker pull ghcr.io/openzim/zimit
	fastapi dev src/zimit_manager/main.py

test:
	docker pull hello-world
	pytest tests
