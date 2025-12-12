def build_acl_commands(acl, mode: str):
    cmds = []

    if mode == "remove":
        if acl.acl_type == "named":
            cmds.append(f"no ip access-list {acl.acl_name}")
        else:
            cmds.append(f"no access-list {acl.acl_number}")
        return cmds

    # CREATE MODE
    if acl.acl_type == "standard":
        cmds.append(
            f"access-list {acl.acl_number} {acl.action} {acl.ip_address} {acl.wildcard}"
        )

    elif acl.acl_type == "extended":
        cmds.append(
            f"access-list {acl.acl_number} {acl.action} {acl.protocol} {acl.ip_address} {acl.wildcard} {acl.dest_ip} {acl.dest_wildcard}"
        )

    elif acl.acl_type == "named":
        cmds.append(f"ip access-list extended {acl.acl_name}")
        cmds.append(f"{acl.action} {acl.protocol} {acl.ip_address} {acl.wildcard} {acl.dest_ip} {acl.dest_wildcard}")

    return cmds
