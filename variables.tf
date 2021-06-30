# Input variable definitions

variable "users_filename" {
  description = "User file name"
  type        = string
  default     = "users.json"
}

variable "markdown_filename" {
  description = "The filename of the markdown file that is going to be generated"
  type        = string
  default     = "users.md"
}

