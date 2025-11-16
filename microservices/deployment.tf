# ***************** Universidad de los Andes ***********************
# ****** Departamento de Ingeniería de Sistemas y Computación ******
# ********** Arquitectura y diseño de Software - ISIS2503 **********
#
# Infraestructura para laboratorio de Microservicios
#
# Elementos a desplegar en AWS:
# 1. Grupos de seguridad:
#    - msd-traffic-api (puerto 8080)
#    - msd-traffic-apps (puerto 8080)
#    - msd-traffic-db (puerto 5432)
#    - cbd-traffic-ssh (puerto 22)
#
# 2. Instancias EC2:
#    - msd-variables-db (PostgreSQL instalado y configurado)
#    - msd-measurements-db (PostgreSQL instalado y configurado)
#    - msd-variables-ms (Servicio de variables descargado)
#    - msd-measurements-ms (Servicio de measurements instalado y configurado)
#    - msd-kong (Kong API Gateway instalado y configurado)
# ******************************************************************

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

# Recurso. Define el grupo de seguridad para el tráfico del API gateway (8000).
resource "aws_security_group" "traffic_api" {
    name        = "${var.project_prefix}-traffic-api"
    description = "Allow application traffic on port 8000"

    ingress {
        description = "HTTP access for gateway layer"
        from_port   = 8000
        to_port     = 8000
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = merge(local.common_tags, {
        Name = "${var.project_prefix}-traffic-api"
    })
}

# Recurso. Define el grupo de seguridad para el tráfico de los microservicios (8080).
resource "aws_security_group" "traffic_apps" {
    name        = "${var.project_prefix}-traffic-apps"
    description = "Allow application traffic on port 8080"

    ingress {
        description = "HTTP access for service layer"
        from_port   = 8080
        to_port     = 8080
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = merge(local.common_tags, {
        Name = "${var.project_prefix}-traffic-apps"
    })
}

# Recurso. Define el grupo de seguridad para el tráfico de las bases de datos (5432).
resource "aws_security_group" "traffic_db" {
  name        = "${var.project_prefix}-traffic-db"
  description = "Allow PostgreSQL access"

  ingress {
    description = "Traffic from anywhere to DB"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-traffic-db"
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

# Recurso. Define la instancia EC2 para la base de datos PostgreSQL de variables.
# Esta instancia incluye un script de creación para instalar y configurar PostgreSQL.
# El script crea un usuario y una base de datos, y ajusta la configuración para permitir conexiones remotas.
resource "aws_instance" "variables_db" {
  ami                         = "ami-051685736c7b35f95"
  instance_type               = var.instance_type
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.traffic_db.id, aws_security_group.traffic_ssh.id]

  user_data = <<-EOT
              #!/bin/bash

              docker run --restart=always -d -e POSTGRES_USER=variables_user -e POSTGRES_DB=variables_db -e POSTGRES_PASSWORD=isis2503 -p 5432:5432 --name variables-db postgres
              EOT

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-variables-db"
    Role = "variables-db"
  })
}

# Recurso. Define la instancia EC2 para la base de datos PostgreSQL de measurements.
# Esta instancia incluye un script de creación para instalar y configurar PostgreSQL.
# El script crea un usuario y una base de datos, y ajusta la configuración para permitir conexiones remotas.
resource "aws_instance" "measurements_db" {
  ami                         = "ami-051685736c7b35f95"
  instance_type               = var.instance_type
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.traffic_db.id, aws_security_group.traffic_ssh.id]

  user_data = <<-EOT
              #!/bin/bash

              docker run --restart=always -d -e POSTGRES_USER=measurements_user -e POSTGRES_DB=measurements_db -e POSTGRES_PASSWORD=isis2503 -p 5432:5432 --name measurements-db postgres
              EOT

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-measurements-db"
    Role = "measurements-db"
  })
}

# Recurso. Define la instancia EC2 para el microservicio de Vairables (Django).
# Esta instancia incluye un script de creación para instalar el servicio de Variables.
resource "aws_instance" "variables_ms" {
  ami                         = "ami-051685736c7b35f95"
  instance_type               = var.instance_type
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.traffic_apps.id, aws_security_group.traffic_ssh.id]

  user_data = <<-EOT
              #!/bin/bash

              sudo dnf install nano git -y

              mkdir -p /labs
              cd /labs

              if [ ! -d ISIS2503-Microservices-AppDjango ]; then
                git clone ${local.repository}
              fi

              cd ISIS2503-Microservices-AppDjango/variables
              sudo sed -i "s/<VARIABLES_DB_HOST>/${aws_instance.variables_db.private_ip}/g" Dockerfile
              EOT

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-variables-ms"
    Role = "variables-ms"
  })

  depends_on = [aws_instance.variables_db]
}

# Recurso. Define la instancia EC2 para el microservicio de Measurements (Django).
# Esta instancia incluye un script de creación para instalar el microservicio de Measurements y aplicar las migraciones.
resource "aws_instance" "measurements_ms" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.traffic_apps.id, aws_security_group.traffic_ssh.id]

  user_data = <<-EOT
              #!/bin/bash

              export MEASUREMENTS_DB_HOST=${aws_instance.measurements_db.private_ip}
              echo "MEASUREMENTS_DB_HOST=${aws_instance.measurements_db.private_ip}" | sudo tee -a /etc/environment

              export VARIABLES_HOST=${aws_instance.variables_ms.private_ip}
              echo "VARIABLES_HOST=${aws_instance.variables_ms.private_ip}" | sudo tee -a /etc/environment

              sudo apt-get update -y
              sudo apt-get install -y python3-pip git build-essential libpq-dev python3-dev

              mkdir -p /labs
              cd /labs

              if [ ! -d ISIS2503-Microservices-AppDjango ]; then
                git clone ${local.repository}
              fi
              
              cd ISIS2503-Microservices-AppDjango/measurements

              sudo pip3 install --upgrade pip --break-system-packages
              sudo pip3 install -r requirements.txt --break-system-packages

              sudo python3 manage.py makemigrations
              sudo python3 manage.py migrate
              EOT

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-measurements-ms"
    Role = "measurements-ms"
  })

  depends_on = [aws_instance.measurements_db, aws_instance.variables_ms]
}

# Recurso. Define la instancia EC2 para Kong (API Gateway).
resource "aws_instance" "kong" {
  ami                         = "ami-051685736c7b35f95"
  instance_type               = var.instance_type
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.traffic_api.id, aws_security_group.traffic_ssh.id]

  user_data = <<-EOT
              #!/bin/bash

              sudo export VARIABLES_HOST=${aws_instance.variables_ms.private_ip}
              echo "VARIABLES_HOST=${aws_instance.variables_ms.private_ip}" | sudo tee -a /etc/environment
              sudo export MEASUREMENTS_HOST=${aws_instance.measurements_ms.private_ip}
              echo "MEASUREMENTS_HOST=${aws_instance.measurements_ms.private_ip}" | sudo tee -a /etc/environment


              sudo dnf install nano git -y
              sudo mkdir /labs
              cd /labs
              sudo git clone https://github.com/ISIS2503/ISIS2503-Microservices-AppDjango.git
              cd ISIS2503-Microservices-AppDjango

              # Configurar el archivo kong.yaml con las IPs de los microservicios

              sudo sed -i "s/<VARIABLES_HOST>/${aws_instance.variables_ms.private_ip}/g" kong.yaml
              sudo sed -i "s/<MEASUREMENTS_HOST>/${aws_instance.measurements_ms.private_ip}/g" kong.yaml
              docker network create kong-net
              docker run -d --name kong --network=kong-net --restart=always \
              -v "$(pwd):/kong/declarative/" -e "KONG_DATABASE=off" \
              -e "KONG_DECLARATIVE_CONFIG=/kong/declarative/kong.yaml" \
              -p 8000:8000 kong/kong-gateway
              EOT

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-kong"
    Role = "api-gateway"
  })

  depends_on = [aws_instance.variables_ms, aws_instance.measurements_ms]
}

# Salida. Muestra la dirección IP pública de la instancia de Kong (API Gateway).
output "kong_public_ip" {
  description = "Public IP address for the Kong API Gateway instance"
  value       = aws_instance.kong.public_ip
}

# Salida. Muestra las direcciones IP públicas de la instancia de Variables MS.
output "variables_ms_public_ip" {
  description = "Public IP address for the Variables Microservice instance"
  value       = aws_instance.variables_ms.public_ip
}

# Salida. Muestra las direcciones IP públicas de la instancia de Measurements MS.
output "measurements_ms_public_ip" {
  description = "Public IP address for the Measurements Microservice instance"
  value       = aws_instance.measurements_ms.public_ip
}

# Salida. Muestra las direcciones IP privadas de la instancia de la base de datos de Variables.
output "variables_db_private_ip" {
  description = "Private IP address for the Variables Database instance"
  value       = aws_instance.variables_db.private_ip
}

# Salida. Muestra las direcciones IP privadas de la instancia de la base de datos de Measurements.
output "measurements_db_private_ip" {   
  description = "Private IP address for the Measurements Database instance"
  value       = aws_instance.measurements_db.private_ip
}