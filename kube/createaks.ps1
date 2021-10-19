#this is actually powershell not bash
$name = "aksaadrbacvnet"
$location = "uksouth"

az group create -l $location -n $name

az aks create `
    --resource-group $name `
    --location $location `
    --name $name `
    --load-balancer-sku standard `
    --enable-managed-identity `
    --enable-aad `
    --node-count 1 `
    --max-pods 30 `
    --network-plugin azure `
    --node-vm-size standard_b2s `
    --min-count 1 `
    --max-count 3 `
    --enable-cluster-autoscaler 
    
    # --enable-azure-rbac `
    # --attach-acr registrytdv9504 `
    # --vnet-subnet-id "/subscriptions/267ee942-931b-4197-a65c-a232b17acc11/resourceGroups/teamResources/providers/Microsoft.Network/virtualNetworks/vnet/subnets/vm-subnet"   

# Get your AKS Resource ID and get super admin on it
# $AKS_ID=az aks show -g teamResources -n $name --query id -o tsv
# $superadmin = "gabriel@cloudconfusion.co.uk"
# az role assignment create --role "Azure Kubernetes Service RBAC Cluster Admin" --assignee $superadmin --scope $AKS_ID

# create namespaces, create secrets, deploy yamls

az aks get-credentials -g teamResources --name $name
kubectl create namespace api
kubectl create namespace web

kubectl create secret generic newcreds --namespace api --from-literal=SQL_USER="sqladmintDv9504" --from-literal=SQL_PASSWORD="Y9^6Ag%8bu"  --from-literal=SQL_SERVER='sqlservertdv9504.database.windows.net'  --from-literal=SQL_DBNAME='mydrivingDB'

kubectl apply -f poi.yaml
kubectl apply -f trips.yaml
kubectl apply -f tripviewer.yaml
kubectl apply -f user-java.yaml
kubectl apply -f userprofile.yaml

