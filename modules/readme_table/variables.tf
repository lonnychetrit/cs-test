# # Input variable definitions

variable "header_titles" {
  description = "List of keys that we want to be displayed in the markdown table (those keys will be used to generate the table header)"
  type        = list(string)
  default     = [] 
}
variable "column_alignment" {
  description = "List of columns alignment (the column_alignment length has to be the same than the header_titles length)"
  type        = list(string)
  default     = [] 
}
variable "dictionnary_list" {
  description = "List of dictionnaries with which we want to create the README table"
  type        = list(map(any))
  default     = []
}

