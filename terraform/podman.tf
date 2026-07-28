resource "podman_container" "simpleservice" {
  container_host = local.container_host
  name           = "simpleservice_flask"
  image          = "simpleservice_flask"

  env = {
    REMOTE_RANDOM_URL = "http://${var.remote_host}:${var.remote_port}/random"
    DATABASE_USER     = var.database_user
    DATABASE_HOST     = var.database_host
    DATABASE_PORT     = var.database_port
    DATABASE_NAME     = var.database_name
    REDIS_HOST        = var.redis_host
    REDIS_PORT        = var.redis_port
    REDIS_DB          = var.redis_db
    USE_REDIS         = var.use_redis
    DEBUG             = var.debug_service
    USE_OTEL          = var.use_otel
    OTEL_SERVER       = var.otel_host
    OTEL_PORT         = var.otel_port
    PORT              = var.service_port
    WORKERS           = var.workers
  }

  port_mappings = [
    {
      container_port = var.service_port
      host_port      = var.service_port
    }
  ]

  secret_env = {
    DATABASE_PASS = "simpleservice_database_pass"
  }
}

output "captured_container_name" {
  description = "The name of the container that was created"
  value       = podman_container.simpleservice
}
