# Terraform - check_password Module
This terraform module receives a list of passwords and returns a dictionnary with each password as key and a boolean as value (true if the password is secure and false if not)

Input variable example
Variable name: passwords
```
["non_secured_password", "secured_password"]
```

Output example
Output name: passwords
```
{
    "non_secured_password" = false,
    "secured_password" = true
}
```

