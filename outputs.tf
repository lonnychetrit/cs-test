# Output variable definitions

output "test1"{
  value = yamlencode(local.users_to_yaml)
}

output "test2"{
  value = local.sorted_users_by_city
}
output "passwords"{
  value = local.checked_passwords
}

