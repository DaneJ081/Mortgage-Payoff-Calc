# two resource groups, one for staging, one for prod. No registry will be used.
resource "azurerm_resource_group" "example" {
  name     = "${var.prefix}-rg-${var.env}"
  location = "${var.location}"
}

resource "azurerm_log_analytics_workspace" "example" {
  name                = "${var.prefix}-loganalytics-${var.env}"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_container_app_environment" "ca-stg" {
  name                       = "${var.prefix}-caenv-${var.env}"
  location                   = azurerm_resource_group.example.location
  resource_group_name        = azurerm_resource_group.example.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.example.id

}

resource "azurerm_container_app" "example" {
  name                         = "${var.prefix}-ca-${var.env}"
  container_app_environment_id = azurerm_container_app_environment.ca-stg.id
  resource_group_name          = azurerm_resource_group.example.name
  revision_mode                = "Single"

  template {
    container {
      name   = "${var.prefix}-ca"
      image  = "tiggy081/mortcal:latest"
      cpu    = 0.25
      memory = "0.5Gi"
    }
  }
  ingress {
    target_port = 8000
    external_enabled = true
    traffic_weight {
    percentage = 100
    latest_revision = true
    }
  }
}