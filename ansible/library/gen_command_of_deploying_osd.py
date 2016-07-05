#!/usr/bin/python

from ansible.module_utils.basic import *

def main():
    fields = {
        "host": {"required": True, "type": "str"},
        "drives": {"require": True, "type": "list" },
        "journal_drives": {"type": "list" },
        "num_of_osd_on_journal": {"type": "int"},
        "state": {
            "default": "present",
            "choices": ['present', 'absent'],
            "type": 'str'
        },
    }

    module = AnsibleModule(argument_spec=fields)

    fields = module.params
    host = fields['host']
    drives = fields['drives']
    journal_drives = fields['journal_drives']
    num_of_osd = fields['num_of_osd_on_journal']
    num = fields['num_of_osd_on_journal']

    count = 0
    journal_drives_count = 0
    command_list = []

    for drive in fields['drives']:
        if count == num:
            count = 0
            journal_drives_count += 1
        count += 1
        if journal_drives_count > len(journal_drives) - 1:
            command_list.append('ceph-deploy --overwrite-conf osd create --zap-disk {}:{}'.format(host, drive))
        else:
            command_list.append('ceph-deploy --overwrite-conf osd create --zap-disk {}:{}:{}'.format(host, drive, journal_drives[journal_drives_count]))

    response = {
         "result": command_list,
    }
    module.exit_json(changed=False, meta=response)


if __name__ == '__main__':
    main()
