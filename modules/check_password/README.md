# Terraform - check_password Module
This terraform module receives a list of passwords and returns a dictionnary with each password as key and a boolean as value (true if the password is secure and false if not)

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_passwords"></a> [passwords](#input\_passwords) | Password to check | `list(string)` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_passwords"></a> [passwords](#output\_passwords) | dictionnary with each password as key and a boolean as value (true if the password is secure and false if not) |

## Examples

Input variable example
```
passwords=["non_secured_password", "secured_password"]
```

Output example
```
passwords={
    "non_secured_password" = false,
    "secured_password" = true
}
```

## Unit tests
To run the unit test you have to install the pytest package 
https://docs.pytest.org/en/6.2.x/getting-started.html

Once installed use the following command to run the unit tests on this module
```
pytest test/unit_test.py
```

