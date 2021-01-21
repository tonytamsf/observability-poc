# SignalFX Detetors with Terraform Demo
## Run
Create a file named `terraform.tfvars` and add variable values. A sample:
```
auth_token = "signalfx token"
email_address = "me@example.com"
memory_used = 240000000
host_names = ["host1", "host2"]
```
Then `terraform apply`