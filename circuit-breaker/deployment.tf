# ***************** Universidad de los Andes ***********************
# ****** Departamento de Ingeniería de Sistemas y Computación ******
# ********** Arquitectura y diseño de Software - ISIS2503 **********
#
# Infraestructura para laboratorio de Circuit Breaker
#
# Elementos a desplegar en AWS:
# 1. Grupos de seguridad:
#    - cbd-traffic-django (puerto 8080)
#    - cbd-traffic-cb (puertos 8000 y 8001)
#    - cbd-traffic-db (puerto 5432)
#    - cbd-traffic-ssh (puerto 22)
#
# 2. Instancias EC2:
#    - cbd-kong
#    - cbd-db (PostgreSQL instalado y configurado)
#    - cbd-monitoring (Monitoring app instalada y migraciones aplicadas)
#    - cbd-alarms-a (Monitoring app instalada)
#    - cbd-alarms-b (Monitoring app instalada)
#    - cbd-alarms-c (Monitoring app instalada)
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
  default     = "cbd"
}

# Variable. Define el tipo de instancia EC2 a usar para las máquinas virtuales.
variable "instance_type" {
  description = "EC2 instance type for application hosts"
  type        = string
  default     = "t2.nano"
}

# Proveedor. Define el proveedor de infraestructura (AWS) y la región.
provider "aws" {
  region = var.region
}

# Variables locales usadas en la configuración de Terraform.
locals {
  project_name = "${var.project_prefix}-circuit-breaker"
  repository   = "https://github.com/ISIS2503/ISIS2503-MonitoringApp.git"
  branch       = "Circuit-Breaker"

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
        Name = "${var.project_prefix}-traffic-services"
    })
}

# Recurso. Define el grupo de seguridad para el tráfico del Circuit Breaker (8000, 8001).
resource "aws_security_group" "traffic_cb" {
  name        = "${var.project_prefix}-traffic-cb"
  description = "Expose Kong circuit breaker ports"

  ingress {
    description = "Kong traffic"
    from_port   = 8000
    to_port     = 8001
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-traffic-cb"
  })
}

# Recurso. Define el grupo de seguridad para el tráfico de la base de datos (5432).
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

# Recurso. Define la instancia EC2 para Kong (Circuit Breaker).
# Esta instancia se crea planamente sin configuración adicional.
resource "aws_instance" "kong" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.traffic_cb.id, aws_security_group.traffic_ssh.id]

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-kong"
    Role = "circuit-breaker"
  })
}

# Recurso. Define la instancia EC2 para la base de datos PostgreSQL.
# Esta instancia incluye un script de creación para instalar y configurar PostgreSQL.
# El script crea un usuario y una base de datos, y ajusta la configuración para permitir conexiones remotas.
resource "aws_instance" "database" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  associate_public_ip_address = false
  vpc_security_group_ids      = [aws_security_group.traffic_db.id, aws_security_group.traffic_ssh.id]

  user_data = <<-EOT
              #!/bin/bash

              sudo apt-get update -y
              sudo apt-get install -y postgresql postgresql-contrib

              sudo -u postgres psql -c "CREATE USER monitoring_user WITH PASSWORD 'isis2503';"
              sudo -u postgres createdb -O monitoring_user monitoring_db
              echo "host all all 0.0.0.0/0 trust" | sudo tee -a /etc/postgresql/16/main/pg_hba.conf
              echo "listen_addresses='*'" | sudo tee -a /etc/postgresql/16/main/postgresql.conf
              echo "max_connections=2000" | sudo tee -a /etc/postgresql/16/main/postgresql.conf
              sudo service postgresql restart
              EOT

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-db"
    Role = "database"
  })
}

# Recurso. Define las instancias EC2 para el servicio de alarmas de la aplicación de Monitoring.
# Se crean tres instancias (a, b, c) usando un bucle.
# Cada instancia incluye un script de creación para instalar la aplicación de Monitoring.
resource "aws_instance" "alarms" {
  for_each = toset(["a", "b", "c"])

  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.traffic_django.id, aws_security_group.traffic_ssh.id]

  user_data = <<-EOT
              #!/bin/bash
              sudo export DATABASE_HOST=${aws_instance.database.private_ip}
              echo "DATABASE_HOST=${aws_instance.database.private_ip}" | sudo tee -a /etc/environment

              sudo apt-get update -y
              sudo apt-get install -y python3-pip git build-essential libpq-dev python3-dev

              mkdir -p /labs
              cd /labs

              if [ ! -d ISIS2503-MonitoringApp ]; then
                git clone ${local.repository}
              fi

              cd ISIS2503-MonitoringApp
              git fetch origin ${local.branch}
              git checkout ${local.branch}
              sudo pip3 install --upgrade pip --break-system-packages
              sudo pip3 install -r requirements.txt --break-system-packages
              EOT

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-alarms-${each.key}"
    Role = "alarms"
  })
}

# Recurso. Define la instancia EC2 para la aplicación de Monitoring (Django).
# Esta instancia incluye un script de creación para instalar la aplicación de Monitoring y aplicar las migraciones.
resource "aws_instance" "monitoring" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.traffic_django.id, aws_security_group.traffic_ssh.id]

  user_data = <<-EOT
              #!/bin/bash

              sudo export DATABASE_HOST=${aws_instance.database.private_ip}
              echo "DATABASE_HOST=${aws_instance.database.private_ip}" | sudo tee -a /etc/environment

              sudo apt-get update -y
              sudo apt-get install -y python3-pip git build-essential libpq-dev python3-dev

              mkdir -p /labs
              cd /labs

              if [ ! -d ISIS2503-MonitoringApp ]; then
                git clone ${local.repository}
              fi

              cd ISIS2503-MonitoringApp
              git fetch origin ${local.branch}
              git checkout ${local.branch}
              sudo pip3 install --upgrade pip --break-system-packages
              sudo pip3 install -r requirements.txt --break-system-packages

              sudo python3 manage.py makemigrations
              sudo python3 manage.py migrate
              EOT

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-monitoring"
    Role = "monitoring-app"
  })

  depends_on = [aws_instance.database]
}

# Salida. Muestra la dirección IP pública de la instancia de Kong (Circuit Breaker).
output "kong_public_ip" {
  description = "Public IP address for the Kong circuit breaker instance"
  value       = aws_instance.kong.public_ip
}

# Salida. Muestra las direcciones IP públicas de las instancias de la aplicación de alarmas.
output "alarms_public_ips" {
  description = "Public IP addresses for the alarms service instances"
  value       = { for id, instance in aws_instance.alarms : id => instance.public_ip }
}

# Salida. Muestra la dirección IP pública de la instancia de la aplicación de Monitoring.
output "monitoring_public_ip" {
  description = "Public IP address for the monitoring service application"
  value       = aws_instance.monitoring.public_ip
}

# Salida. Muestra las direcciones IP privadas de las instancias de la aplicación de alarmas.
output "alarms_private_ips" {
  description = "Private IP addresses for the alarms service instances"
  value       = { for id, instance in aws_instance.alarms : id => instance.private_ip }
}

# Salida. Muestra la dirección IP privada de la instancia de la aplicación de Monitoring.
output "monitoring_private_ip" {
  description = "Private IP address for the monitoring service application"
  value       = aws_instance.monitoring.private_ip
}

# Salida. Muestra la dirección IP privada de la instancia de la base de datos PostgreSQL.
output "database_private_ip" {
  description = "Private IP address for the PostgreSQL database instance"
  value       = aws_instance.database.private_ip
}
