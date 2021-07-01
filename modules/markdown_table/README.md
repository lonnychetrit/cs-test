# Terraform - readme_table Module
This terraform module can be used to generate markdown table from a list of dictionnaries

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_column_alignment"></a> [column\_alignment](#input\_column\_alignment) | List of columns alignment (the column\_alignment length has to be the same than the header\_titles length) | `list(string)` | n/a | yes |
| <a name="input_dictionnary_list"></a> [dictionnary\_list](#input\_dictionnary\_list) | List of dictionnaries with which we want to create the README table | `list(map(any))` | n/a | yes |
| <a name="input_header_titles"></a> [header\_titles](#input\_header\_titles) | List of keys that we want to be displayed in the markdown table (those keys will be used to generate the table header) | `list(string)` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_markdown_table_string"></a> [markdown\_table\_string](#output\_markdown\_table\_string) | Markdown table string |


## Unit tests
To run the unit test you have to install the pytest package 
https://docs.pytest.org/en/6.2.x/getting-started.html

Once installed use the following command to run the unit tests on this module
```
pytest test/unit_test.py
```