resource "aws_kms_key" "vault" {
  description             = "Master key for vault"
  deletion_window_in_days = 10
}

resource "aws_kms_alias" "vault" {
  name          = "alias/vault"
  target_key_id = "${aws_kms_key.vault.key_id}"
}
