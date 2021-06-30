# Output variable definitions

output "passwords" {
  description = "True if the password is secure and false if not"
  value       = local.passwords
}
