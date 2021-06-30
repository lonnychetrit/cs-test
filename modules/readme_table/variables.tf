# # Input variable definitions

variable "header_titles" {
  description = "List of dictionnaries with which we want to create the README table"
  type        = list(string)
  default     = ["name", "age", "city", "password"] 
}
variable "column_alignment" {
  description = "List of dictionnaries with which we want to create the README table"
  type        = list(string)
  default     = ["left", "center", "left", "right"] 
}
variable "dictionnary_list" {
  description = "List of dictionnaries with which we want to create the README table"
  type        = list(map(any))
  default     = [
        {
            "name": "john",
            "age": 23,
            "city": "barcelona",
            "password": "123456"
        },
        {
            "name": "john",
            "age": 23,
            "city": "barcelona",
            "password": "123456"
        },
        ]
}

