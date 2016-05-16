backend "consul" {
  path        = "vault"
  address     = "consul-0"
  tls_disable = 1
}

listener "tcp" {
  address     = "127.0.0.1:8200"
  tls_disable = 1
}
