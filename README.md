# Vault terraform


## TODO:
- [x] create kms key
- [x] create ami policy:
```json
 {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Stmt1443036478000",
            "Effect": "Allow",
            "Action": [
                "kms:Decrypt",
		"kmd:Encrypt"
            ],
            "Resource": [
                "<your KMS key ARN>"
            ]
        }
    ]
}
```
- [x] launch vault instances
- [x] attach iam role to the instances
- [x] install vault bin
- [ ] cipherblob=$(aws kms encrypt --key-id alias/XXXXXXX --plaintext "$(vault init -key-shares=1 -key-threshold=1 |head -1 |cut -d":" -f 2|xargs)" --query CiphertextBlob --output text)
- [ ] vault -server ....
- [ ] vault unseal $(aws kms decrypt --ciphertext-blob fileb://<(echo $cipherblob | base64 -d) --query Plaintext --output text |base64 -d)


