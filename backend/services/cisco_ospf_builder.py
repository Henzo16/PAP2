def build_ospf_commands(route, mode: str):
    """
    mode = 'create' | 'remove'
    """
    base_cmd = f"network {route.network} {route.wildcard_mask} area {route.area}"

    if mode == "remove":
        return [
            f"router ospf {route.process_id}",
            f"no {base_cmd}"
        ]

    return [
        f"router ospf {route.process_id}",
        base_cmd
    ]
