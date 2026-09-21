FROM python:3.12.13-alpine3.22

LABEL maintainer="cloud-optimisation-and-accountability <CloudOptimisationandAccountabilityTeam@justice.gov.uk>"

# Install system dependencies
RUN apk add --no-cache --no-progress \
  libffi-dev \
  build-base \
  curl \
  groff \
  less \
  jq \
  && apk update \
  && apk upgrade --no-cache --available

# Create user and group
RUN addgroup -S appgroup && adduser -S appuser -G appgroup -u 1051

# Set working directory
WORKDIR /home/coat-coh-dashboard

# Change ownership of the working directory
RUN chown -R appuser:appgroup /home/coat-coh-dashboard

# Switch to non-root user
USER 1051

# Copy Pipfile and Pipfile.lock
COPY --chown=appuser:appgroup requirements.txt ./

# Install dependencies without --system
RUN python3 -m venv .venv && source .venv/bin/activate && \
    pip install -r requirements.txt

# Copy application code
COPY --chown=appuser:appgroup app.py app.py

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8501

# Healthcheck
HEALTHCHECK --interval=60s --timeout=30s CMD curl -I -XGET http://localhost:8501 || exit 1

# Use pipenv to run gunicorn
ENTRYPOINT ["streamlit", "run", "app.py"]