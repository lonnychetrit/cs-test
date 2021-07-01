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

## Unit tests
To run the unit test you have to install the pytest package 
https://docs.pytest.org/en/6.2.x/getting-started.html

Once installed use the following command to run the unit tests on this module
```
pytest test/unit_test.py
```

