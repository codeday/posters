.DEFAULT_GOAL := main

main:
	@rm -rf api/build && cd frontend && npm install && npm run build && cp -rf build ../api

run:
	@cd api && uvicorn main:app --host 0.0.0.0 --port 8000

docker:
	@cd api && python3 tasks.py && rm -rf remote/templates && rm -rf build && cd .. && docker build -t codeday-posters .

run-docker:
	@docker run -it -p "8000:8000" codeday-posters
