kubectl delete ns dev
kubectl delete ns elastic
kubectl delete pv es-dev-pv-volume
kubectl delete pv es-pv-volume
kubectl create ns dev
kubectl create ns elastic
kubectl apply -f elastic_pv.yaml
kubectl apply -f elastic_compose.yaml
helm install wepapp github-test/test --set service.nodePort=30001 --set ElasticSearch=elastic-dev-svc.dev.svc.cluster.local -n dev