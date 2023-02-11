from packaging import version
import os
import operator


ops = {
    "<": operator.lt,
    "<=": operator.le,
    ">=": operator.ge,
    ">": operator.gt,
}


def get_version(tool: str) -> str:
    tool = tool.capitalize()
    output = os.popen('flutter --version').read()
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


if __name__ == '__main__':
    print("flutter version: ", get_version("flutter"))
    print("dart version: ", get_version("dart"), "\n")

    print("project flutter version: ", get_project_version("flutter"))
    print("project dart version: ", get_project_version("dart"), "\n")

    print("compare flutter versions: ", compare_versions(
        get_version("flutter"), get_project_version("flutter")))
    print("compare dart versions: ", compare_versions(
        get_version("dart"), get_project_version("dart")), "\n")
