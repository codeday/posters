.DEFAULT_GOAL := main

main:
	@rm -rf api/build && cd frontend && npm install && npm run build && cp -rf build ../api

run:
	@cd api && uvicorn main:app --host 0.0.0.0 --port 8000
