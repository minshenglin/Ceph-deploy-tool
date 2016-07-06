deploy-tool user guide
======================


This project is for deploying Ceph cluster including:

- Initialize the environment(user, ntp, ufw...)
- Install all package required(Online/Offline/None)
- Deploy ceph cluster
- Set up monitor(Calamari)
- Set up the service gateway(RadosGW, RBD-client)

We use ansible as deploy tool and base on OS 'Ubuntu 16.04'.
Including the feature below:

- Set up /etc/hosts
- Build up password-less sudoer
- Deploy SSH public key
- Stop the service of firewall
- Deploy Ceph cluster(Rados roles, gateway node)
- Initialize Calamari


Step
----

1. Install Ansible(2.1)

> sudo apt-get install ansible -y


2. Be sure about that the ansible's client must:

 + sshpass installed
 + disable the fingerprint of ssh (Add "StrictHostKeyChecking no" in config)

3. Set up general setting

> $ vim ansible/group_vars/all

```
install_mode: none  # online/offline/none

username: ubuntu
password: ubuntu

# change IP if there already have ntp server
ntp_server_ip: "{{ lookup('file', './tmp/ntp_server_ip') }}"
```

  * `install_mode` : The mode of installing packages, there have three modes to choose: **online/offline/none**.

  * `username` : The name of user which is going to create.

  * `password` : The password of user

  * `ntp_server_ip` : Change this if there already have ntp server, or you can set up new ntp server by setting the node IP in **ansible/hosts**.


4. Set up the information of OSD node(OSD disk and journal)

> vim ansible/group_vars/deploy

```
num_of_osd_on_journal: 2

drives_list: [
  {
    host: '',
    drives: [    
    ],
    journal_drives: [
    ],
  },
]
```
example
```
num_of_osd_on_journal: 2

drives_list: [
  {
    host: 'osd-node0',
    drives: [
      '/dev/sda',
      '/dev/sdb',
    ],
    journal_drives: [
      '/dev/sdc',
    ],
  },
  {
    host: 'osd-node1',
    drives: [
      '/dev/sda',
      '/dev/sdb',
    ],
    journal_drives: [
      '/dev/sdc',
    ],
  },
]
```

5. Set up the information of host (IP)

> $ vim ansible/hosts

```
[monitor]
[osd]
[deploy]
[ntp-server]
[calamari-server]
[radosgw]
[client]
```

6. Launch the command to run the playbook

> $ ansible-playbook site.yml -i hosts --ask-pass --ask-sudo-pass
