# Output variable definitions

output "passwords" {
  description = "dictionnary with each password as key and a boolean as value (true if the password is secure and false if not)"
  value       = local.passwords
}
