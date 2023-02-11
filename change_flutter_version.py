from packaging import version
import os
import operator

main_flutter_path = os\
    .popen("where flutter")\
    .read()\
    .splitlines()[0]\
    .strip()\
    .replace(f"{os.sep}bin{os.sep}flutter", "")

path = main_flutter_path\
    .replace(f"{os.sep}flutter", "")

ops = {
    "<": operator.lt,
    "<=": operator.le,
    ">=": operator.ge,
    ">": operator.gt,
}


def get_version(tool: str, flutter: str = "flutter") -> str:
    tool = tool.capitalize()
    output = os.popen(f"{flutter} --version").read()
    return output.split()[output.split().index(tool) + 1]


def get_project_version(tool: str) -> str:
    tool = tool.lower() + ":"

    with open("pubspec.lock", "r", encoding="utf-8") as f:
        data = f.read()

    sdks = False
    for line in data.splitlines():
        if line.strip() == "sdks:":
            sdks = True
        if sdks and line.strip().startswith(tool):
            return line.replace(tool, "").strip().strip('"')


def compare_versions(v1: str, v2s: str) -> bool:
    output = []

    if not v2s:
        return True

    for v2 in v2s.split():
        delete = [str(x) for x in range(10)] + ["."]
        operator = "".join([x for x in v2 if not x in delete])

        v2 = v2.strip(operator)
        output.append(ops[operator](version.parse(v1), version.parse(v2)))

    return not False in output


def get_flutters():
    data = {}
    for i in os.listdir(path):
        flutter_path = os.path.join(path, i, "bin", "flutter")
        # 'flutter': 'flutter version,dart version',
        data[flutter_path] = f'{get_version("flutter", flutter_path)},{get_version("dart", flutter_path)}'
    return data


if __name__ == '__main__':
    flutter_version = get_version("flutter")
    dart_version = get_version("dart")
    project_flutter_version = get_project_version("flutter")
    project_dart_version = get_project_version("dart")

    print("flutter version:", flutter_version)
    print("dart version:", dart_version, "\n")

    print("project flutter version:", project_flutter_version)
    print("project dart version:", project_dart_version, "\n")

    compare_flutter = compare_versions(flutter_version, get_project_version("flutter"))
    compare_dart = compare_versions(dart_version, get_project_version("dart"))

    print("compare flutter versions:", compare_flutter)
    print("compare dart versions:", compare_dart, "\n")

    if not compare_flutter or not compare_dart:
        flutters = get_flutters()
        a = 1
        for i in flutters:
            name = i.split(os.sep)[-3]
            flutter_version_loop = flutters[i].split(',')[0]
            dart_version = flutters[i].split(',')[1]

            compare_flutter = compare_versions(get_version("flutter", i), get_project_version("flutter"))
            compare_dart = compare_versions(get_version("dart", i), get_project_version("dart"))

            print(f"({a}) {name}:\n\tflutter version: {flutter_version_loop}\n\tdart version: {dart_version}\n\n\tcompare flutter version: {compare_flutter}\n\tcompare dart version: {compare_dart}\n")
            a += 1
        
        new_flutter = input("enter the number of the flutter version you want to use: ")
        new_flutter = list(flutters.keys())[int(new_flutter) - 1].replace(f"{os.sep}bin{os.sep}flutter", "")

        if new_flutter == main_flutter_path:
            print("the flutter version you selected is the same as the current one")
            exit()

        os.rename(main_flutter_path, f"{main_flutter_path}-{flutter_version}")
        os.rename(new_flutter, main_flutter_path)

        print("new flutter version:", get_version("flutter", new_flutter))
