# Terraform configuration


locals{
    # Converting the first letter of each word to uppercase.
    header_titles = [for value in var.header_titles: title(value)]
    # Joining the header titles to create the markdown table header
    header_titles_line = "|${join("|", local.header_titles)}|"
    # Creating the alignment line
    alignment = [for value in var.column_alignment: replace(replace(replace(value, "left", ":--"), "right", "--:"), "center", ":--:")]
    alignment_line = "|${join("|", local.alignment)}|"
    # Creating the table content
    table_data = [ for object in var.dictionnary_list: "|${join("|", [for key in var.header_titles: object[key]])}|"]
    # Concatenating all the table lines into a single list
    readme_table = concat([local.header_titles_line], [local.alignment_line], local.table_data)
    # Adding breaklines after each row
    readme_table_string = join("\n", local.readme_table)
}



