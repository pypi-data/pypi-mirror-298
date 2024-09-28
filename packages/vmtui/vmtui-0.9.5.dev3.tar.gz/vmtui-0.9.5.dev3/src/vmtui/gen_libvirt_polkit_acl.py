#!/usr/bin/env python
__author__    = "Christian Gruhl"
__license__   = ""
__copyright__ = "© 2024"
__version__   = "0.9.5"

import argparse
import yaml

polkit_admin_padding = "        "
polkit_acl_padding = "                    "
polkit_admin_placeholder = "%:ADMIN_GRP:%"
polkit_acl_placeholder = "%:ACL_DEFS:%"
polkit_template = """

polkit.addRule(function(action, subject) {
    if (
%s
        false // makes generation easier
       ) {
        if (action.id == "org.libvirt.unix.manage" || action.id.startsWith("org.libvirt.api")) {
            return polkit.Result.YES;
        }

        } else if ( subject.isInGroup("user_vm") ) {
            if (action.id == "org.libvirt.unix.manage" || action.id.startsWith("org.libvirt.api.connect")) {
                return polkit.Result.YES;
            } else if (action.id.startsWith("org.libvirt.api.domain") && action.lookup("connect_driver")=="QEMU") {
                var dom = action.lookup("domain_name");
                if(
%s
                    false // makes generation easier
                ) {
                    return polkit.Result.YES;
                    } else {
                    return polkit.Result.NO;
                }
            } else if ( action.id.startsWith("org.libvirt.api.network") ) {
                if ( action.id.endsWith("getattr") ||
                     action.id.endsWith("read") ||
                     action.id.endsWith("create")
                    ) {
                    return polkit.Result.YES;
                } else {
                    return polkit.Result.NO;
                }
            }
    }
        return polkit.Result.NO;
}
);

""" %  (polkit_admin_placeholder, polkit_acl_placeholder)

def arguments():
    parser = argparse.ArgumentParser("Generate polkit Access Control Lists for libvirtd")
    parser.add_argument('-c', '--acl', type=str, default="/etc/libvirt_acl.yaml", help="Path to the ACL file. Files are only written if the are not empty.")
    parser.add_argument('-o', '--rules', type=str, default="/etc/polkit-1/rules.d/100-libvirt-access.rules", help="Path to the output ACL rule file")
    return parser.parse_args()

def main():

    args = arguments()
    
    with open(args.acl) as stream:
        try:
            db = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)
            return -1
        
    libvirt_admin_acls = db["libvirt_acl"].get("admin_groups")
    admin_definitions = ""
    if libvirt_admin_acls is not None:
        for adm_grp in libvirt_admin_acls:
            ac_entry = f"subject.isInGroup(\"{adm_grp}\") ||"
            admin_definitions += polkit_admin_padding + ac_entry + "\n"
        
    policy = polkit_template.replace(polkit_admin_placeholder, admin_definitions)
    
    

    libvirt_dom_acls = db["libvirt_acl"].get("domains")
    acl_definitions = ""
    if libvirt_dom_acls is not None:
        for domain in libvirt_dom_acls:        
            for user in libvirt_dom_acls[domain].get("users", []):
                ac_entry = f"(dom == \"{domain}\" && subject.user == \"{user}\") ||"
                acl_definitions += polkit_acl_padding + ac_entry + "\n"
            for group in libvirt_dom_acls[domain].get("groups", []):
                ac_entry = f"(dom == \"{domain}\" && subject.isInGroup(\"{group}\")) ||"
                acl_definitions += polkit_acl_padding + ac_entry + "\n"

    policy = policy.replace(polkit_acl_placeholder, acl_definitions)

    with open(args.rules, "w") as rule:
        rule.write(policy)
    
if __name__ == "__main__":
    main()
