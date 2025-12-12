def build_static_route_commands(route, mode: str):
    """
    mode = "create" | "remove"
    """
    cmd = f"ip route {route.network} {route.mask} {route.next_hop}"

    if mode == "remove":
        return [f"no {cmd}"]

    return [cmd]
