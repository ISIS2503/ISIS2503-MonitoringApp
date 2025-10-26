# ***************** Universidad de los Andes ***********************
# ****** Departamento de Ingeniería de Sistemas y Computación ******
# ********** Arquitectura y diseño de Software - ISIS2503 **********
#
# Infraestructura para laboratorio de base de datos NoSQL (MongoDB)
#
# Elementos a desplegar en AWS:
# 1. Grupos de seguridad:
#    - nosqld-traffic-django (puerto 8080)
#    - nosqld-traffic-db (puerto 5432)
#    - nosqld-traffic-ssh (puerto 22)
#
# 2. Instancias EC2:
#    - nosqld-mongo (ECS-Optimized Amazon Linux 2023  sin MongoDB)
#    - nosqld-django-no-patterns (repositorio clonado y requerimientos instalados)
#    - nosqld-django-patterns (repositorio clonado y requerimientos instalados)
# ******************************************************************

# Variable. Define la región de AWS donde se desplegará la infraestructura.
variable "region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-east-1"
}

# Variable. Define el prefijo usado para nombrar los recursos en AWS.
variable "project_prefix" {
  description = "Prefix used for naming AWS resources"
  type        = string
  default     = "nosqld"
}

# Variable. Define el tipo de instancia EC2 a usar para las máquinas virtuales.
variable "instance_type" {
  description = "EC2 instance type for application hosts"
  type        = string
  default     = "t3.micro"
}

# Proveedor. Define el proveedor de infraestructura (AWS) y la región.
provider "aws" {
  region = var.region
}

# Variables locales usadas en la configuración de Terraform.
locals {
  project_name = "${var.project_prefix}-nosql"
  repository   = "https://github.com/ISIS2503/ISIS2503-MonitoringAppNoSQL.git"

  common_tags = {
    Project   = local.project_name
    ManagedBy = "Terraform"
  }
}

# Data Source. Busca la AMI más reciente de Ubuntu 24.04 usando los filtros especificados.
data "aws_ami" "ubuntu" {
    most_recent = true
    owners      = ["099720109477"]

    filter {
        name   = "name"
        values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
    }

    filter {
        name   = "virtualization-type"
        values = ["hvm"]
    }
}

# Recurso. Define el grupo de seguridad para el tráfico de Django (8080).
resource "aws_security_group" "traffic_django" {
    name        = "${var.project_prefix}-traffic-django"
    description = "Allow application traffic on port 8080"

    ingress {
        description = "HTTP access for service layer"
        from_port   = 8080
        to_port     = 8080
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = merge(local.common_tags, {
        Name = "${var.project_prefix}-traffic-django"
    })
}

# Recurso. Define el grupo de seguridad para el tráfico de la base de datos MongoDB (27017).
resource "aws_security_group" "traffic_mongo" {
  name        = "${var.project_prefix}-traffic-mongo"
  description = "Allow MongoDB access"

  ingress {
    description = "Traffic from anywhere to DB"
    from_port   = 27017
    to_port     = 27017
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-traffic-mongo"
  })
}

# Recurso. Define el grupo de seguridad para el tráfico SSH (22) y permite todo el tráfico saliente.
resource "aws_security_group" "traffic_ssh" {
  name        = "${var.project_prefix}-traffic-ssh"
  description = "Allow SSH access"

  ingress {
    description = "SSH access from anywhere"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-traffic-ssh"
  })
}

# Recurso. Define la instancia EC2 para la base de datos MongoDB.
resource "aws_instance" "mongo" {
  ami                         = "ami-051685736c7b35f95"
  instance_type               = var.instance_type
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.traffic_mongo.id, aws_security_group.traffic_ssh.id]

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-mongo"
    Role = "mongodb-database"
  })
}

# Recurso. Define la instancia EC2 para la aplicación de Monitoring (Django) sin patrones para la base de datos.
# Esta instancia incluye un script de creación para instalar la aplicación de Monitoring.
resource "aws_instance" "django_no_patterns" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.traffic_django.id, aws_security_group.traffic_ssh.id]

  user_data = <<-EOT
              #!/bin/bash

              sudo apt-get update -y
              sudo apt-get install -y python3-pip git build-essential libpq-dev python3-dev

              mkdir -p /labs
              cd /labs

              if [ ! -d ISIS2503-MonitoringAppNoSQL ]; then
                git clone ${local.repository}
              fi

              cd ISIS2503-MonitoringAppNoSQL
              sudo git checkout nosql-no-patterns
              sudo pip3 install --upgrade pip --break-system-packages
              sudo pip3 install -r requirements.txt --break-system-packages
              EOT

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-django-no-patterns"
    Role = "monitoring-app-no-patterns"
  })

  depends_on = [aws_instance.mongo]
}

# Recurso. Define la instancia EC2 para la aplicación de Monitoring (Django) con patrones para la base de datos.
# Esta instancia incluye un script de creación para instalar la aplicación de Monitoring.
resource "aws_instance" "django_patterns" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.traffic_django.id, aws_security_group.traffic_ssh.id]

  user_data = <<-EOT
              #!/bin/bash

              sudo apt-get update -y
              sudo apt-get install -y python3-pip git build-essential libpq-dev python3-dev

              mkdir -p /labs
              cd /labs

              if [ ! -d ISIS2503-MonitoringAppNoSQL ]; then
                git clone ${local.repository}
              fi

              cd ISIS2503-MonitoringAppNoSQL
              sudo git checkout nosql-patterns
              sudo pip3 install --upgrade pip --break-system-packages
              sudo pip3 install -r requirements.txt --break-system-packages
              EOT

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-django-patterns"
    Role = "monitoring-app-patterns"
  })

  depends_on = [aws_instance.mongo]
}

# Salida. Muestra la dirección IP pública de la instancia de la aplicación de Monitoring sin patrones.
output "monitoring_no_patterns_public_ip" {
  description = "Public IP address for the monitoring service application without patterns"
  value       = aws_instance.django_no_patterns.public_ip
}

# Salida. Muestra la dirección IP pública de la instancia de la aplicación de Monitoring con patrones.
output "monitoring_patterns_public_ip" {
  description = "Public IP address for the monitoring service application with patterns"
  value       = aws_instance.django_patterns.public_ip
}

# Salida. Muestra la dirección IP privada de la instancia de la base de datos MongoDB.
output "mongo_private_ip" {
  description = "Private IP address for the MongoDB database instance"
  value       = aws_instance.mongo.private_ip
}
