# AWS Permissions and roles not set, this build is meant for AWS Academy with Vocareum
data "aws_iam_role" "lab_role" {
  name = "LabRole"
}

data "aws_lambda_function" "authorizer" {
  function_name = "authorizer"
}

data "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  tags = {
  "Name" = "app_vpc" }
}

data "aws_subnet" "public_subnet_1" {
  vpc_id     = data.aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
}

data "aws_subnet" "public_subnet_2" {
  vpc_id     = data.aws_vpc.main.id
  cidr_block = "10.0.2.0/24"
}

data "aws_subnet" "private_subnet_1" {
  vpc_id     = data.aws_vpc.main.id
  cidr_block = "10.0.3.0/24"
}

data "aws_subnet" "private_subnet_2" {
  vpc_id     = data.aws_vpc.main.id
  cidr_block = "10.0.4.0/24"
}
