terraform {
  required_providers {
    podman = {
      source = "decafcode/podman"
    }

    local = {
      source  = "hashicorp/local"
      version = "~> 2.4.0"
    }
  }
}

locals {
  container_host = "unix:///var/run/user/1000/podman/podman.sock"
}
