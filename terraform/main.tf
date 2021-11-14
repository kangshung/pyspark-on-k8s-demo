terraform {
  required_providers {
    linode = {
      source  = "linode/linode"
      version = "1.23.0"
    }
  }
}

provider "linode" {
  token = var.token
}

resource "linode_lke_cluster" "pyspark-demo-k8s-cluster" {
  label       = "pyspark-demo-k8s-cluster"
  k8s_version = "1.21"
  region      = "eu-central"
  tags        = ["prod"]

  pool {
    type  = "g6-standard-4"
    count = 3
  }
}

resource "linode_instance" "pyspark-demo-nfs-server" {
  label           = "pyspark-demo-nfs-server"
  image           = "linode/debian10"
  region          = "eu-central"
  type            = "g6-standard-2"
  authorized_keys = [
    "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDB+umgZeJtiRllbCg8psqhq79s+5fUMcpXHptYsGL8LA16I+6oyphMK4tk4EYjCQJ5NU9wZzZ7zyT2+56FnjG6nutmAeuw0lsJAfIqZ4VYv7C4BlevZBeuDO/tfwaZDSdvxyYA9UCrl49nfvwVvN6g6UC2x8ur+kGP0bWYkFrjfvGIPDyvZRZ6J7dnXXqIpc/Q0N5e3qhILXBBwFwwCUB2FQ1rNKT2cLrwotralTdBofaS+32X+ZIjAMQ90ANNN+sU2SZs92HZvNduEL+q1BlGBXOdGxiydHgEuGC1+u5mgqNXZ5oBS2IPgEevsClgJ2xCjZ+WP82EQeqQyGhMp327oUvqmlnvZbIC9cEyn4OVUDFxrvPnWfiC3SulCSOppqgKYQ1WTxD+556YCPiyh2bxvHW/8rSBg/54mSt2A20qvRHIA14t+O+sif/ElwfDDwFR512zSXLOUwOUmDi76nULElMpzhv8iL3NH7NAHZzvgmOa5kwfl7T9ouyPwZr0S9s= damian@DESKTOP-RPD95IG"
  ]
  root_pass       = "PqvTGQoAV7RWYYkh"
  swap_size       = 256
  private_ip      = true
}

output "pyspark-demo-nfs-server-ip" {
  value = linode_instance.pyspark-demo-nfs-server.ip_address
}
