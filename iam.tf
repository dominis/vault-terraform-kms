resource "aws_iam_instance_profile" "vault" {
  name  = "vault"
  roles = ["${aws_iam_role.kms.id}"]
}

resource "aws_iam_role" "kms" {
  name = "kms"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "kms.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "kms" {
  name = "kms encrypt/decrypt"
  role = "${aws_iam_role.kms.id}"

  policy = <<EOF
 {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Stmt1443036478000",
            "Effect": "Allow",
            "Action": [
                "kms:Decrypt",
                "kms:Encrypt"
            ],
            "Resource": [
                "${aws_kms_key.vault.arn}"
            ]
        }
    ]
}EOF
}
