resource "aws_security_group" "app_api_sg" {
  name        = "app-api-sg"
  description = "Security group for RDS"
  vpc_id      = data.aws_vpc.main.id

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
