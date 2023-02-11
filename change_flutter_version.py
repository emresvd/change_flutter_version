from packaging import version
import os
import operator

path = os\
    .popen("where flutter")\
    .read()\
    .splitlines()[0]\
    .strip()\
    .replace(f"{os.sep}flutter{os.sep}bin{os.sep}flutter", "")

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
    print("flutter version:", get_version("flutter"))
    print("dart version:", get_version("dart"), "\n")

    print("project flutter version:", get_project_version("flutter"))
    print("project dart version:", get_project_version("dart"), "\n")

    compare_flutter = compare_versions(get_version("flutter"), get_project_version("flutter"))
    compare_dart = compare_versions(get_version("dart"), get_project_version("dart"))

    print("compare flutter versions:", compare_flutter)
    print("compare dart versions:", compare_dart, "\n")

    if not compare_flutter or not compare_dart:
        flutters = get_flutters()
        for i in flutters:
            name = i.split(os.sep)[-3]
            flutter_version = flutters[i].split(',')[0]
            dart_version = flutters[i].split(',')[1]

            compare_flutter = compare_versions(get_version("flutter", i), get_project_version("flutter"))
            compare_dart = compare_versions(get_version("dart", i), get_project_version("dart"))

            print(f"{name}:\n\tflutter version: {flutter_version}\n\tdart version: {dart_version}\n\tcompare flutter version: {compare_flutter}\n\tcompare dart version: {compare_dart}\n")
