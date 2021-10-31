##name of resource group and aks cluster and location
$name = "tfregkubeblob"
$location = "uksouth"



##cluster admin usergroup creation and id of the cluster admin
az group create -l $location -n $name
$clusteradminuser = "gabriel@cloudkingdoms.com"
$clusteradminuserid = az ad user show --id $clusteradminuser --query objectId --output tsv



$clusteradmingroupname = "AKSclusteradmins"
$clusteradmingroupid = az ad group create  --display-name $clusteradmingroupname --mail-nickname $clusteradmingroupname --description "admin group for AKS clusters" --query objectId --output tsv
az ad group member add --group $clusteradmingroupid --member-id $clusteradminuserid 


##create cluster, including cluster admin assign group
az aks create `
    --resource-group $name `
    --location $location `
    --aad-admin-group-object-ids $clusteradmingroupid `
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

az aks get-credentials -g $name --name $name

#nginx install
kubectl.exe apply -f .\kube\ingress\nginxingress.yaml
#nginx install (where got it from)
#kubectl.exe apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v0.40.2/deploy/static/provider/cloud/deploy.yaml

#wait for the public IP to come for DNS 
$IP = (kubectl.exe get service ingress-nginx-controller --namespace ingress-nginx --output=json |ConvertFrom-Json).status.loadBalancer.ingress.ip
# Name to associate with public IP address
$DNSNAME="terraform-reg-gm"
# Get the resource-id of the public ip
$PUBLICIPID=$(az network public-ip list --query "[?ipAddress!=null]|[?contains(ipAddress, '$IP')].[id]" --output tsv)
# Update public ip address with DNS nv
az network public-ip update --ids $PUBLICIPID --dns-name $DNSNAME

#cert manager
https://artifacthub.io/packages/helm/cert-manager/cert-manager
kubectl.exe create namespace cert-manager
kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.5.4/cert-manager.crds.yaml
helm repo add jetstack https://charts.jetstack.io
helm install certmanageraks jetstack/cert-manager `
--namespace cert-manager `
--version v1.5.4  `
--set nodeSelector."kubernetes\.io/os"=linux 
#  --set installCRDs=true ` don't need this because of installing it seprate. 
#the above sometimes seems to hang the window and needs some returns to shake free

kubectl.exe apply -f .\kube\app.yaml
kubectl.exe apply -f .\kube\cert-manager\certclusterissuerandingress.yaml
kubectl.exe get cert --all-namespaces  #wait for it to switch to true
then go here
# Display the FQDN
az network public-ip show --ids $PUBLICIPID --query "[dnsSettings.fqdn]" --output tsv
