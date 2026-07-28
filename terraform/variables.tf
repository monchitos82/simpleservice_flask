variable "remote_host" {
  description = "The hostname for a remote API downstream"
  type        = string
  default     = "host.containers.internal"
}

variable "database_host" {
  description = "The hostname for the database server"
  type        = string
  default     = "host.containers.internal"
}

variable "redis_host" {
  description = "The hostname for the redis server"
  type        = string
  default     = "host.containers.internal"
}

variable "otel_host" {
  description = "The hostname for the otel collector"
  type        = string
  default     = "host.containers.internal"
}

variable "service_port" {
  description = "Service port to map on the container"
  type        = number
  default     = 5200
}

variable "remote_port" {
  description = "Remote API downstream port"
  type        = number
  default     = 5200
}

variable "database_port" {
  description = "Database server port"
  type        = number
  default     = 5432
}

variable "redis_port" {
  description = "Redis server port"
  type        = number
  default     = 6379
}

variable "otel_port" {
  description = "Otel collector port"
  type        = number
  default     = 4317
}
