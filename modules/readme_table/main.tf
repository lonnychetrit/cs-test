# Terraform configuration


locals{
    header_titles = [for value in var.header_titles: title(value)]
    header_titles_line = "|${join("|", local.header_titles)}|"
    alignment = [for value in var.column_alignment: replace(replace(replace(value, "left", ":--"), "right", "--:"), "center", ":--:")]
    alignment_line = "|${join("|", local.alignment)}|"
    table_data = [ for object in var.dictionnary_list: "|${join("|", [for key in var.header_titles: object[key]])}|"]
    readme_table = concat([local.header_titles_line], [local.alignment_line], local.table_data)
    readme_table_string = join("\n", local.readme_table)

}



