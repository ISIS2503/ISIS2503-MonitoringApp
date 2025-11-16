# ***************** Universidad de los Andes ***********************
# ****** Departamento de Ingeniería de Sistemas y Computación ******
# ********** Arquitectura y diseño de Software - ISIS2503 **********
#
# Infraestructura para laboratorio de microservicios con FastAPI (microservicio Places)
# Elementos a desplegar en AWS:
# 1. Grupos de seguridad:
#    - msd-traffic-mongodb (puerto 27017)
# 2. Instancias EC2:
#    - msd-places-db (mongodb instalado y configurado)
#    - msd-places-ms (Servicio de places instalado y configurado)

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.18.0"
    }
  }
}

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
  default     = "msd"
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
  project_name = "${var.project_prefix}-microservices"
  repository   = "https://github.com/ISIS2503/ISIS2503-Microservices-AppDjango.git"

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

# Recurso. Define el grupo de seguridad para el tráfico de los microservicios (8080).
resource "aws_security_group" "traffic_apps" {
    name        = "${var.project_prefix}-traffic-apps-places"
    description = "Allow application traffic on port 8080"

    ingress {
        description = "HTTP access for service layer"
        from_port   = 8080
        to_port     = 8080
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = merge(local.common_tags, {
        Name = "${var.project_prefix}-traffic-apps-places"
    })
}

# Recurso. Define el grupo de seguridad para el tráfico SSH (22) y permite todo el tráfico saliente.
resource "aws_security_group" "traffic_ssh" {
  name        = "${var.project_prefix}-traffic-ssh-places"
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
    Name = "${var.project_prefix}-traffic-ssh-places"
  })
}

# Recurso. Define el grupo de seguridad para el tráfico de MongoDB.
resource "aws_security_group" "traffic_mongodb" {
    name        = "${var.project_prefix}-traffic-mongodb"
    description = "Allow application traffic on port 27017"

    ingress {
        description = "MongoDB access for database layer"
        from_port   = 27017
        to_port     = 27017
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = merge(local.common_tags, {
        Name = "${var.project_prefix}-traffic-mongodb"
    })
}

# Recurso. Define la instancia EC2 para la base de datos de Places (MongoDB).
# Esta instancia se crea planamente sin configuración adicional.
resource "aws_instance" "places_db" {
  ami                         = "ami-051685736c7b35f95"
  instance_type               = var.instance_type
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.traffic_mongodb.id, aws_security_group.traffic_ssh.id]

  user_data = <<-EOT
              #!/bin/bash

              docker run --restart=always -d --name places-db -p 27017:27017 \
                            -e MONGO_INITDB_ROOT_USERNAME=monitoring_user \
                            -e MONGO_INITDB_ROOT_PASSWORD=isis2503 \
                            mongodb/mongodb-community-server
              EOT

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-places-db"
    Role = "places-db"
  })
}

# Recurso. Define la instancia EC2 para el microservicio de Places (FastAPI).
# Esta instancia incluye un script de creación para instalar el microservicio de Places y aplicar las migraciones.
resource "aws_instance" "places_ms" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.traffic_apps.id, aws_security_group.traffic_ssh.id]

  user_data = <<-EOT
              #!/bin/bash

              sudo export PLACES_DB_HOST=${aws_instance.places_db.private_ip}
              echo "PLACES_DB_HOST=${aws_instance.places_db.private_ip}" | sudo tee -a /etc/environment

              sudo apt-get update -y
              sudo apt-get install -y python3-pip git build-essential libpq-dev python3-dev

              mkdir -p /labs
              cd /labs

              if [ ! -d ISIS2503-Microservices-AppDjango ]; then
                git clone ${local.repository}
              fi
              
              cd ISIS2503-Microservices-AppDjango/places

              sudo apt install -y python3.12-venv
              sudo python3 -m venv venv
              sudo venv/bin/pip install -r requirements.txt

              EOT

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-places-ms"
    Role = "places-ms"
  })

  depends_on = [aws_instance.places_db]
}

# Salida. Muestra la dirección IP privada de la instancia de places_db (MongoDB).
output "places_db_private_ip" {
  description = "Private IP address for the Places Database instance"
  value       = aws_instance.places_db.private_ip
}

# Salida. Muestra las direcciones IP públicas de la instancia de Places MS.
output "places_ms_public_ip" {
  description = "Public IP address for the Places Microservice instance"
  value       = aws_instance.places_ms.public_ip
}