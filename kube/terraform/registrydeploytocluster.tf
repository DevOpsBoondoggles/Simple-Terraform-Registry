data "azurerm_kubernetes_cluster" "aks" {
  name                = azurerm_kubernetes_cluster.k8s.name
  resource_group_name = azurerm_resource_group.k8s.name
}

provider "kubernetes" {
  host                   = data.azurerm_kubernetes_cluster.aks.kube_admin_config.0.host
  client_certificate     = base64decode(data.azurerm_kubernetes_cluster.aks.kube_admin_config.0.client_certificate)
  client_key             = base64decode(data.azurerm_kubernetes_cluster.aks.kube_admin_config.0.client_key)
  cluster_ca_certificate = base64decode(data.azurerm_kubernetes_cluster.aks.kube_admin_config.0.cluster_ca_certificate)
}

resource "kubernetes_namespace" "terraform" {
  metadata {
    name = "terraform"
  }
}

resource "kubernetes_namespace" "ingress" {
  metadata {
    name = "ingress-tf"
  }
}

resource "kubernetes_namespace" "cert-man" {
  metadata {
    name = "cert-manager"
  }
}

##trying with helm

provider "helm" {
  kubernetes {
    host                   = data.azurerm_kubernetes_cluster.aks.kube_admin_config.0.host
    client_certificate     = base64decode(data.azurerm_kubernetes_cluster.aks.kube_admin_config.0.client_certificate)
    client_key             = base64decode(data.azurerm_kubernetes_cluster.aks.kube_admin_config.0.client_key)
    cluster_ca_certificate = base64decode(data.azurerm_kubernetes_cluster.aks.kube_admin_config.0.cluster_ca_certificate)
  }
  
}


resource "helm_release" "nginx" {
  name       = "nginx-ingress"
  repository = "https://kubernetes.github.io/ingress-nginx"
  chart      = "ingress-nginx"
  namespace = kubernetes_namespace.ingress.metadata[0].name
  set {
    name = "controller.replicaCount"
    value = 2
  }
  # set {
  #   name = "controller.nodeSelector.\"kubernetes.io/os\""
  #   value = "linux"
  # }
}


resource "helm_release" "cert-manager" {
  name       = "cert-manager"
  repository = "https://charts.jetstack.io"

  chart      = "cert-manager"
  version = "v1.5.4"
  namespace = kubernetes_namespace.cert-man.metadata[0].name
  set {
    name = "installCRDs"
    value = "true"
  }
  set {
    name = "controller.nodeSelector.\"kubernetes\\.io/os\""
    value = "linux"
  }
}


output "helmngin" {
  value = helm_release.nginx.set
  sensitive = true
}

output "helmcert" {
  value = helm_release.cert-manager.set
  sensitive = true
}