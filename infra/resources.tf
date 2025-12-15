resource "azurerm_resource_group" "rg" {
  name     = "${var.prefix}-rg-${var.env}"
  location = var.location
}

resource "azurerm_log_analytics_workspace" "law" {
  name                = "${var.prefix}-loganalytics-${var.env}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_container_app_environment" "cae" {
  name                       = "${var.prefix}-containerenv-${var.env}"
  location                   = azurerm_resource_group.rg.location
  resource_group_name        = azurerm_resource_group.rg.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.law.id

}

resource "azurerm_container_app" "ca" {
  name                         = "${var.prefix}-containerapp-${var.env}"
  container_app_environment_id = "azurerm_container_app_environment.cae-${var.env}.id"
  resource_group_name          = azurerm_resource_group.rg.name
  revision_mode                = "Single"

  template {
    container {
      name   = "${var.prefix}-containerapp"
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