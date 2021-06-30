# Terraform configuration

# resource "local_file" "foo" {
#     content     = "foo!"
#     filename = "${path.module}/foo.bar"
# }

# -------------------------------------------

locals {
  users = jsondecode(file("${path.module}/${var.users_filename}"))
  users_with_password = { "users":[for i, user in local.users["users"] : merge(user, {"password": random_string.random[i].result}) ]}
  # test1
  users_to_yaml = {
      "users": flatten(
      # Flattening the final result as we want a list and not a list of lists
        # Going through all the users 
        [for user_key, user in local.users_with_password["users"]: 
          # Going through all the users keys
          [for user_key_name, user_key_value in user: 
            # Structuring the final desired result
            {
              "key": "user[${user_key}].${user_key_name}",
              "value": user_key_value
            }
          ]
        ]
      )
    }

  # test2
  users_cities = [for key in local.users_to_yaml["users"]: key if length(regexall("^user[[0-9]+].city$", key["key"])) > 0]
  test2 = { for city in local.users_cities: city.value => {for key, value in local.users_to_yaml["users"]: split(".",value.key)[1] => value.value if split(".",value.key)[0] == split(".",city.key)[0] && split(".",value.key)[1] != "city"}...}
  age_per_city_test = {for city_name, users in local.test2: city_name => [for user_key, user in users: tonumber("${user.age}.${user_key}")]}
  # age_per_city = {for city_name, users in local.test2: city_name => sort([for user_key, user in users: tonumber("${user.age}.${user_key}")])}
  # sorted_test2 = {for city_name, age in local.age_per_city: city_name => [for age_id in age: local.test2[city_name][split(".", age_id)[1]] ]}

}

output "users_cities"{
  value = local.users_cities
}
output "test2"{
  value = local.test2
}
output "age_per_city"{
  value = sort([1,10,2,3,4])
}


resource "random_string" "random" {
  length           = 8
  count = length(local.users["users"])
}

# module "readme_table" {
#   source = "./modules/readme_table"

#   users_filename = var.users_filename

# }

# module "check_pwd" {
#   source = "./modules/check_password"
#   passwords = ["lonnyf", "_Lf))ONN1Y%LONNYLON2)45NY1"]

# }

# resource "local_file" "users_to_readme_table" {
#     content  = local.content
#     filename = var.users_filename
# }