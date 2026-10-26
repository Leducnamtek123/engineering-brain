variable "env" {
  type    = string
  default = terraform.workspace
}

resource "aws_ecs_cluster" "main" {
  name = "shop-${var.env}"
}

resource "aws_ecs_service" "api" {
  name          = "api-${var.env}"
  cluster       = aws_ecs_cluster.main.id
  desired_count = var.env == "prod" ? 3 : 1
}

resource "aws_lb" "public" {
  name = "shop-${var.env}"
}

resource "aws_db_instance" "main" {
  identifier          = "shop-${var.env}"
  engine              = "postgres"
  instance_class      = var.env == "prod" ? "db.r6g.large" : "db.t4g.micro"
  skip_final_snapshot = var.env != "prod"
}

resource "aws_s3_bucket" "uploads" {
  bucket = "shop-uploads-${var.env}"
}
