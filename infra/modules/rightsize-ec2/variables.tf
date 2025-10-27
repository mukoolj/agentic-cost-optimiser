variable "region" {
  type        = string
  default     = "ap-southeast-2"
  description = "AWS region"
}

variable "desired_instance_types" {
  description = "Map of instance_id => new_instance_type"
  type        = map(string)
  default     = {}
}
