def max_cut(filename):
    vertices = []
    edges = []
    mode = None

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line == "V":
                mode = "V"
                continue
            if line == "E":
                mode = "E"
                continue
            if mode == "V":
                v = line.strip("()")
                vertices.append(v)
            elif mode == "E":
                part = line.split("-")
                u = part[0].strip("()")
                v = part[1].strip("()")
                w = int(part[2])
                edges.append(((u, v), w))

    return vertices, edges
