terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}
provider "aws" { region = "us-east-1" }
resource "aws_ecr_repository" "app" {
  name = "trading-copilot"
  image_tag_mutability = "IMMUTABLE"
  image_scanning_configuration { scan_on_push = true }
}
resource "aws_cloudwatch_log_group" "app" {
  name = "/trading-copilot/app"
  retention_in_days = 14
}
output "repository_url" { value = aws_ecr_repository.app.repository_url }
