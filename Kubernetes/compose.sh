# kubectl delete ns dev
# kubectl delete ns elastic
# kubectl delete pv es-dev-pv-volume
# kubectl delete pv es-pv-volume
kubectl create ns dev
kubectl create ns deploy
kubectl create ns elastic
kubectl apply -f Elasticsearch-pv.yaml
kubectl apply -f Elasticsearch-compose.yaml
kubectl apply -f jenkins-pv.yaml
kubectl apply -f jenkins-compose.yaml
docker compose -f gitlab-docker-compose.yaml -d

# For dev namespace
helm install wepapp github-webanalysis/webanalysis --set service.nodePort=30001 --set ElasticSearch=elastic-dev-svc.dev.svc.cluster.local -n dev
