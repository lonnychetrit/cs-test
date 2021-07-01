# Output variable definitions

output "test1"{
  description = "First question of the test"
  value = yamlencode(local.users_to_yaml)
}

output "test2"{
  description = "Second question of the test"
  value = local.sorted_users_by_city
}

