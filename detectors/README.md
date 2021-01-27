# SignalFX Detetors with Terraform Demo
## Run
Create a file named `terraform.tfvars` and add variable values. A sample:
```
auth_token = "signalfx token"
credential_id = "victorops integration id"
routing_key = "victorops routing key"
memory_used = 240000000
host_names = ["host1", "host2"]
```
Then `terraform apply`