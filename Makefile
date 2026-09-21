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

helm-deploy:
	helm upgrade coat-coh-dashboard \
        helm/coat-coh-dashboard \
        --install \
        --force \
        --wait \
        --timeout 10m \
        --namespace coat-coh-dashboard-dev \
        --values=helm/coat-coh-dashboard/values-dev.yaml \
        --set app.deployment.image.repository=levgorbunov1/coat-coh-dashboard \
        --set app.deployment.image.tag=v0.1

helm-uninstall:
	helm uninstall coat-coh-dashboard --namespace coat-coh-dashboard-dev

push-dockerhub:
	docker login
	docker buildx build \
		--platform linux/amd64 \
		-t levgorbunov1/coat-coh-dashboard:v0.1 \
		--push .