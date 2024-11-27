gcloud auth configure-docker
docker build -t us-docker.pkg.dev/your-project-id/your-repo/cloud-run-server .
docker push us-docker.pkg.dev/your-project-id/your-repo/cloud-run-server
