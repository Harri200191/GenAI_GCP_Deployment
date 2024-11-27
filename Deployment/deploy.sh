gcloud run deploy cloud-run-server \
    --image us-docker.pkg.dev/your-project-id/your-repo/cloud-run-server \
    --region your-region \
    --platform managed \
    --allow-unauthenticated \
    --memory 2Gi
