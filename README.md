deploy-tool user guide
-----------

This project is for deploying Ceph cluster including:

- initialize the environment
- install all package required
- deploy ceph cluster
- set up monitor(calamari)
- set up the service gateway

We use ansible as deploy tool and base on OS 'Ubuntu 16.04'.
Including the feature below:

- Build up password-less sudoer
- Deploy SSH public key
- Set up /etc/hosts
- Cancel SELinux
- Stop the service of firewall


Step
----

1. Install Ansible(2.0.1)
```
sudo apt-get install ansible -y
```

2. Set up the information of host
```
vim ansible/hosts
# [deploy]
# [ceph-node]
...
...
```

3. Launch the command to run the playbook
```
ansible-playbook site.yml -i hosts --ask-pass --ask-sudo-pass
```
