# Terraform configuration

# Question 1 - Users manipulation

# Resource that is going to be used to generate users passwords
resource "random_string" "random" {
  length           = 8
  count = length(local.users["users"])
}

locals {
  # Loading users
  users = jsondecode(file("${path.module}/${var.users_filename}"))
  # Generating a password for each user
  users_with_password = {
    "users": [
      for i, user in local.users["users"]:
        merge(user, {"password": random_string.random[i].result}) 
      ]
    }

  # test1
  users_to_yaml = {
      "users": flatten(
      # Flattening the final result because we want a list and not a list of lists
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
  # Extracting only the users cities
  # Output example:
    # users_cities = [
      # {
      #   "key" = "user[0].city"
      #   "value" = "barcelona"
      # }...
    # ]
  users_cities = [for key in local.users_to_yaml["users"]: key if length(regexall("^user[[0-9]+].city$", key["key"])) > 0]

  # Grouping all the users by city
  # Output example:
    # unsorted_users_by_city = {
    #   "barcelona" = [
    #   {
    #     "age" = 23
    #     "name" = "john"
    #     "password" = "!C>x}Tp{"
    #   },
    #   ...
    #   ]
    # }
  unsorted_users_by_city = { for city in local.users_cities: city.value => {for key, value in local.users_to_yaml["users"]: split(".",value.key)[1] => value.value if split(".",value.key)[0] == split(".",city.key)[0] && split(".",value.key)[1] != "city"}...}
  
  # Extracting all user ages by city concatenated with the index of its position in the city list
  # The ages list is then sorted 
  # Output example:
    # ages_by_city = {
    #   "barcelona" = [
    #    "12.1", --> this means that the user which is stored at the position 1 of the "barcelona" list is 12 old
    #    "23.0",
    #    "24.2",
    #    "30.3",
    #   ]
    #   ...
    # }
  ages_by_city = {for city_name, users in local.unsorted_users_by_city: city_name => sort([for user_key, user in users: "${user.age}.${user_key}"])}
  
  # Now that we have the users positions sorted by age we can reconstruct the final result
  # Output example:
    # sorted_users_by_city = {
    #   "barcelona" = [
    #     {
    #       "age" = 12
    #       "name" = "Jonny"
    #       "password" = "JJQ_5Njm"
    #     },
    #     ...
    # }
  sorted_users_by_city = {for city_name, age in local.ages_by_city: city_name => [for age_id in age: local.unsorted_users_by_city[city_name][split(".", age_id)[1]] ]}

}


# Question 2 - Markdown generation

locals {
  # Extracting all the password to send them to security check
  passwords = flatten([for city, users in local.sorted_users_by_city: [for user in users: user["password"]]])
  checked_passwords = module.check_pwd.passwords
  table_to_convert_in_markdown = flatten([for city, users in local.sorted_users_by_city: [for user in users: 
    {
       "name"= user["name"],  
       "age"= user["age"],  
       "city"= city,  
       "password"= local.checked_passwords[user["password"]],  
    }]])
}

module "readme_table" {
  source = "./modules/readme_table"
  header_titles = ["name", "age", "city", "password"]
  column_alignment = ["left", "center", "left", "right"]
  dictionnary_list = local.table_to_convert_in_markdown
}

module "check_pwd" {
  source = "./modules/check_password"
  passwords = local.passwords
}

resource "local_file" "users_to_readme_table" {
    content  = module.readme_table.readme_table_string
    filename = var.markdown_filename
}