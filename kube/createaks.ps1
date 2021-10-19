##name of resource group and aks cluster and location
$name = "aksaadrbacvnet"
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

