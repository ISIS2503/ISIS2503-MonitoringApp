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
