.PHONY: generate deploy clean refresh
.DEFAULT_GOAL := main

main: generate

generate: generate_API

generate_API:
	@echo "Building API Image..."
	@docker build ./API/ --no-cache -t srnd/posters-api-fast
	@echo "API is built"

# generate_react:
# 	@echo "Building Flask Image..."
# 	@docker build . -t @srnd/posters-api-fast

deploy: deploy_API

deploy_API:
	@docker run -d --name posters-api-fast -p 50:8000 srnd/posters-api-fast:latest

clean: docker_clean_API

docker_clean_API:
	@docker stop posters-api-fast
	@docker rm posters-api-fast

refresh: generate clean deploy