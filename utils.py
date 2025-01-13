import numpy as np

def bfs(root, callback, args):
    queue = [root]
    while queue:
        node = queue.pop(0)
        callback(node, args)
        queue.extend(node)

def readnode(node, args):
    if "path" in node.tag:
        data = node.attrib["d"]
        commands = ["M", "l", "L", "Q", "C", "A", "S", "H", "V", "T", "Z", "z"]
        data = data.replace(",", " ")
        for c in commands:
            data = data.replace(c, c+" ")
        fields = [ f for f in data.split(" ") if len(f)>0 ]
        skip = 0
        for i in range(0, len(fields)):
            field = fields[i]
            if skip > 0:
                skip -= 1
                continue
            
            if field not in commands:
                command = last_command
                skip -= 1
                i -= 1
            else:
                command = field
                last_command = command

            if command == "M":
                x = float(fields[i+1])
                y = float(fields[i+2])
                point = np.array([x, y])
                args["points"].append(point)
                skip += 2
            elif command == "l":
                x = float(fields[i+1])
                y = float(fields[i+2])
                point = np.array([x, y])
                args["points"].append(point + args["points"][-1])
                skip += 2
            elif command == "L":
                x = float(fields[i+1])
                y = float(fields[i+2])
                point = np.array([x, y])
                args["points"].append(point)
                skip += 2
            elif command == "Q":
                x1 = float(fields[i+1])
                y1 = float(fields[i+2])
                x2 = float(fields[i+3])
                y2 = float(fields[i+4])
                print("Quadratic Bezier to", x1, y1, x2, y2)
                skip += 4
            elif command == "C":
                x1 = float(fields[i+1])
                y1 = float(fields[i+2])
                x2 = float(fields[i+3])
                y2 = float(fields[i+4])
                x3 = float(fields[i+5])
                y3 = float(fields[i+6])
                print("Bezier curve to", x1, y1, x2, y2, x3, y3)
                skip += 6
            elif command == "A":
                rx = float(fields[i+1])
                ry = float(fields[i+2])
                x_axis_rotation = float(fields[i+3])
                large_arc_flag = float(fields[i+4])
                sweep_flag = float(fields[i+5])
                x = float(fields[i+6])
                y = float(fields[i+7])
                print("Elliptical arc to", rx, ry, x_axis_rotation, large_arc_flag, sweep_flag, x, y)
                skip += 7
            elif command == "S":
                x2 = float(fields[i+1])
                y2 = float(fields[i+2])
                x3 = float(fields[i+3])
                y3 = float(fields[i+4])
                print("Smooth Bezier curve to", x2, y2, x3, y3)
                skip += 4
            elif command == "H":
                x = float(fields[i+1])
                print("Horizontal line to", x)
                skip += 1
            elif command == "V":
                y = float(fields[i+1])
                print("Vertical line to", y)
                skip += 1
            elif command == "T":
                x = float(fields[i+1])
                y = float(fields[i+2])
                print("Smooth quadratic Bezier to", x, y)
                skip += 2
            elif command == "Z" or command == "z":
                pass