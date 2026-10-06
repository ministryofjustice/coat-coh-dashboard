# COAT Cost Optimisation Hub (COH) Dashboard
Dashboard for displaying Cost Optimisation Hub recommendations. Deployed to EKS.

To run the Streamlit application locally:
```
make run-local DASHBOARD=coh_dashboard
```

To run the Docker container:
```
make build DASHBOARD=coh_dashboard
make run DASHBOARD=coh_dashboard
```

To stop the container:
```
make stop DASHBOARD=coh_dashboard
```