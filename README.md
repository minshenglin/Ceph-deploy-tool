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

 + there have sudoer user on each server
 + sshpass installed
 + disable the fingerprint of ssh (Add "StrictHostKeyChecking no" in config)

3. Set up general setting

> $ vim ansible/group_vars/all

```
install_mode: none  # online/offline/none

system_user: ubuntu
system_user_password: ubuntu

user: cephtest
password: cephtest
password_encrypted: isDXdHnlEi7PU
# This user, which is sudoer, is for client to manage Ceph cluster.
# Because of setting user password need to use encrypted string, so we need to gen password
# by command: "python -c 'import crypt; print crypt.crypt("cephtest", "isobuildercool")'"

# change IP if there already have ntp server
ntp_server_ip: "{{ lookup('file', './tmp/ntp_server_ip') }}"
```

  * `install_mode` : The mode of installing packages, there have three modes to choose: **online/offline/none**.

  * `system_user` : The user for initializing and deploy cluster.

  * `system_user_password` : The password of systen user.

  * `user` : The name of user which is for end user to manage the cluster.

  * `password` : The password of user.

  * `password_encrypted` : The encryped password from 'password' by command **python -c 'import crypt; print crypt.crypt("cephtest", "isobuildercool")'**. It's needed for creating user.

  * `ntp_server_ip` : Change this if there already have ntp server, or you can set up new ntp server by setting the node IP in **ansible/hosts**.


4. Set up the information of Ceph deployment

> vim ansible/group_vars/deploy

```
# setting of ceph configuration
public_network: #192.168.1.0/24
cluster_network: #192.168.2.0/24
osd_pool_default_size: 3
osd_pool_default_min_size: 2
osd_pool_default_pg_num: 8
osd_journal_size: 2048 #MB
osd_crush_chooseleaf_type: 1 #host

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
# setting of ceph configuration
public_network: 192.168.1.0/24
cluster_network: 192.168.2.0/24
osd_pool_default_size: 3
osd_pool_default_min_size: 2
osd_pool_default_pg_num: 8
osd_journal_size: 2048 #MB
osd_crush_chooseleaf_type: 1 #host

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

example
```
[monitor]
192.168.1.10

[osd]
192.168.1.11
192.168.1.12
192.168.1.13

[deploy]
192.168.1.10

[ntp-server]
192.168.1.10

[calamari-server]
192.168.1.10

[radosgw]
[client]
```

6. Launch the command to run the playbook

> $ ansible-playbook site.yml -i hosts --ask-pass
