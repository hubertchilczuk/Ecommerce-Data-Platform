variable "project" {
  type        = string
  default     = "ecommerce-data-platform"
  description = "Project identifier used as a prefix for resources."
}

variable "env" {
  type        = string
  default     = "dev"
  description = "Deployment environment (dev / prod)."
}

variable "region" {
  type        = string
  default     = "eu-central-1"
  description = "Cloud region."
}
