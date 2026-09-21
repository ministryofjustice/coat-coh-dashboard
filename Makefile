run-local:
	python3 -m venv .venv && source .venv/bin/activate
	pip install -r requirements.txt
	streamlit run app.py

build:
	docker build -t coat-coh-dashboard:v0.1 .

run:
	docker run -d -p 8501:8501 --name coat-coh-dashboard coat-coh-dashboard:v0.1

stop:
	docker rm -f coat-coh-dashboard