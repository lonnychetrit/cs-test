# Content Square - Devops test

To run the terraform please run the following:
```
terraform init
terraform plan
terraform apply
```

## Providers

| Name | Version |
|------|---------|
| <a name="provider_local"></a> [local](#provider\_local) | n/a |
| <a name="provider_random"></a> [random](#provider\_random) | n/a |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_check_pwd"></a> [check\_pwd](#module\_check\_pwd) | ./modules/check_password | n/a |
| <a name="module_markdown_table"></a> [markdown\_table](#module\_markdown\_table) | ./modules/markdown_table | n/a |

## Resources

| Name | Type |
|------|------|
| [local_file.users_to_readme_table](https://registry.terraform.io/providers/hashicorp/local/latest/docs/resources/file) | resource |
| [random_string.random](https://registry.terraform.io/providers/hashicorp/random/latest/docs/resources/string) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_markdown_filename"></a> [markdown\_filename](#input\_markdown\_filename) | The filename of the markdown file that is going to be generated | `string` | `"users.md"` | no |
| <a name="input_users_filename"></a> [users\_filename](#input\_users\_filename) | Users file name | `string` | `"users.json"` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_test1"></a> [test1](#output\_test1) | First question of the test |
| <a name="output_test2"></a> [test2](#output\_test2) | Second question of the test |
