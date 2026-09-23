run-local:
	python3 -m venv .venv && source .venv/bin/activate
	pip install -r requirements.txt
	streamlit run ./app/app.py

build:
	docker build -t coat-coh-dashboard:v0.1 .

run:
	docker run -d -p 8501:8501 \
		--name coat-coh-dashboard \
		-e AUTH0_DOMAIN="${AUTH0_DOMAIN}" \
		-e AUTH0_CLIENT_ID="${AUTH0_CLIENT_ID}" \
		-e AUTH0_CLIENT_SECRET="${AUTH0_CLIENT_SECRET}" \
		-e APP_BASE_URL="http://localhost:8501" \
		-e APP_ENV="local" \
		coat-coh-dashboard:v0.1

stop:
	docker rm -f coat-coh-dashboard

helm-deploy:
	helm upgrade coat-coh-dashboard \
        helm/coat-coh-dashboard \
        --install \
        --force \
		--server-side=false \
        --wait \
        --timeout 10m \
        --namespace coat-coh-dashboard-dev \
        --values=helm/coat-coh-dashboard/values-dev.yaml \
        --set app.deployment.image.repository=levgorbunov1/coat-coh-dashboard \
        --set app.deployment.image.tag=v0.1 \
		--set app.deployment.env.AUTH0_DOMAIN="${AUTH0_DOMAIN}" \
		--set app.deployment.env.AUTH0_CLIENT_ID="${AUTH0_CLIENT_ID}" \
        --set app.deployment.env.AUTH0_CLIENT_SECRET="${AUTH0_CLIENT_SECRET}" \
		--set app.deployment.env.APP_BASE_URL=coat-coh-dashboard-dev.cloud-platform.service.justice.gov.uk

helm-uninstall:
	helm uninstall coat-coh-dashboard --namespace coat-coh-dashboard-dev

push-dockerhub:
	docker build -t levgorbunov1/coat-coh-dashboard:v0.1 .
	docker login
	docker buildx build \
		--platform linux/amd64 \
		-t levgorbunov1/coat-coh-dashboard:v0.1 \
		--push .