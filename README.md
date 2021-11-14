# pyspark-demo

```bash
terraform apply --var-file secret.tfvars
```

```bash
helm upgrade -i spark ../spark-on-k8s-operator/charts/spark-operator-chart \
  --namespace spark --create-namespace \
  --kubeconfig pyspark-demo-k8s-cluster-kubeconfig.yaml \
  --set webhook.enable=true --set image.repository="gcr.io/spark-operator/spark-operator" --set image.tag="v1beta2-1.2.3-3.1.1"
```

```bash
export KUBECONFIG=pyspark-demo-k8s-cluster-kubeconfig.yaml
kubectl create secret generic google-cloud-key --from-file=key.json=/home/damian/keys/pyspark-demo-project-b311f4c34d16.json -n spark
kubectl create cm log4j --from-file=log4j.properties=k8s/doge/log4j.properties -n spark
kubectl apply -f src/main/k8s/historyserver-deploy.yaml -n spark
```

```bash
apt update \
  && apt install nfs-kernel-server rsync -y \
  && mkdir -p /nfs/share/demo/dags \
  && mkdir -p /nfs/share/demo/logs \
  && chown nobody:nogroup /nfs/share/demo/dags \
  && chown nobody:nogroup /nfs/share/demo/logs \
  && chmod 777 /nfs/share/demo/dags \
  && chmod 777 /nfs/share/demo/logs \
  && echo "/nfs/share/demo/dags  *(rw,sync,no_subtree_check)" >> /etc/exports \
  && echo "/nfs/share/demo/logs  *(rw,sync,no_subtree_check)" >> /etc/exports \
  && exportfs -a \
  && exportfs -v \
  && systemctl restart nfs-kernel-server
```

```bash
sshpass -p 'PqvTGQoAV7RWYYkh' rsync -avP dags/ root@172.104.159.90:/nfs/share/demo/dags

kubectl apply -f src/main/k8s/nfs-pv-pvc.yaml -n airflow
kubectl apply -f src/main/k8s/airflow-worker-rbac.yaml

helm upgrade -i airflow ../airflow/chart \
  --namespace airflow --create-namespace \
  --kubeconfig pyspark-demo-k8s-cluster-kubeconfig.yaml \
  -f src/main/k8s/my-airflow-values.yaml
```




deploy spark-doge:
- secret i log4j
- bez shuffle, bez coalesce, bez cache (pokazac historyserver)
- z shuffle, bez coalesce, bez cache
- z shuffle, z coalesce, bez cache
- z shuffle, z coalesce, z cache

schedulowanie:
- pokazac spark-pi-schedule
- deploy airflow