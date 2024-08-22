#!/bin/sh
# first, if minikube is not already running, then we want to start it

if [ ! $(minikube status | grep "host: Running" | wc -l) -eq 1 ]; then
  minikube start
fi
eval $(minikube docker-env)
docker build -t customer-support:latest .
kubectl apply -f infrastructure/argocd/argocd-ns.yaml
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl apply -f infrastructure/application/app-argo.yaml
kubectl apply -f infrastructure/monitoring/monitoring-argo.yaml
kubectl apply -f infrastructure/database/database-argo.yaml
# kubectl apply -f infrastructure/message-queue/rabbitmq-argo.yaml
# kubectl apply -f infrastructure/message-queue/rabbitmq-argo.yaml
kubectl apply -f infrastructure/argocd/argocd-app.yaml
kubectl apply -f infrastructure/argocd/argocd-clusterrole.yaml
kubectl apply -f infrastructure/argocd/argocd-clusterrolebinding.yaml

# next, we wait for the service to be ready then return the link to localhost where we can access the ArgoCD UI with a nice message to click on the link
echo "Waiting for ArgoCD to be ready..."
kubectl wait --for=condition=available --timeout=1200s deployment/argocd-server -n argocd
argocd admin initial-password -n argocd
echo "ArgoCD is ready to use. Click on the link below to access the ArgoCD UI and log in using admin and initial password from above"
minikube service -n argocd argocd-server --url &
kubectl port-forward -n database svc/postgres 5432:5432 &
kubectl port-forward -n application svc/customer-support 8000:8000 &

wait
