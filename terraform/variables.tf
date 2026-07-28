variable "remote_host" {
  description = "The hostname for a remote API downstream"
  type        = string
  default     = "host.containers.internal"
}

variable "remote_port" {
  description = "The port for a remote API downstream"
  type        = number
  default     = 5200
}

variable "database_host" {
  description = "The hostname for the database server"
  type        = string
  default     = "host.containers.internal"
}

variable "database_port" {
  description = "The port for the database server"
  type        = number
  default     = 5432
}

variable "database_name" {
  description = "The db name for the service"
  type        = string
  default     = "simpleservice"
}

variable "database_user" {
  description = "The db user for the service"
  type        = string
  default     = "simpleservice"
}

variable "use_redis" {
  description = "Enable redis usage"
  type        = bool
  default     = true
}

variable "redis_host" {
  description = "The hostname for the redis server"
  type        = string
  default     = "host.containers.internal"
}

variable "redis_port" {
  description = "Redis server port"
  type        = number
  default     = 6379
}

variable "redis_db" {
  description = "Redis server database"
  type        = number
  default     = 0
}

variable "use_otel" {
  description = "Enable OTEL usage"
  type        = bool
  default     = true
}

variable "otel_host" {
  description = "The hostname for the otel collector"
  type        = string
  default     = "host.containers.internal"
}

variable "otel_port" {
  description = "Otel collector port"
  type        = number
  default     = 4317
}

variable "service_port" {
  description = "Service port to map on the container"
  type        = number
  default     = 5200
}

variable "debug_service" {
  description = "Run the service in debug mode"
  type        = bool
  default     = false
}

variable "workers" {
  description = "Number of service workers to use"
  type        = number
  default     = 2
}
