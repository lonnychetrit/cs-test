# Terraform configuration

locals{
    # Going through each password and attach true if the password is secure and false if not
    passwords = {for password in var.passwords: password => length(password) >= 10 && length(regexall("[a-z]+", password)) > 0 && length(regexall("[0-9].*[0-9]", password)) > 0 && length(regexall("(\\!|\\@|\\#|\\$|\\%|\\&|\\*|\\(|\\))", password)) > 0 && length(regexall("(\\-|\\_|\\=|\\+|\\[|\\]|\\{|\\}|\\<|\\>|\\:|\\?)", password)) == 0 ? true : false} 
}

