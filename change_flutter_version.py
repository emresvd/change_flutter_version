from packaging import version
import os


def returnable_exec(command):
    exec('global i; i = %s' % command)
    global i
    return i


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


def compare_versions(v1: str, v2: str) -> bool:
    delete = [str(x) for x in range(10)] + ["."]
    operator = "".join([x for x in v2 if not x in delete])


def control_version(tool: str, project: bool) -> bool:
    tool = tool.lower()

    version = get_version(tool)
    project_version = get_project_version(tool)

    if project:
        project_version = project_version.split()


if __name__ == '__main__':
    print("flutter version: ", get_version("flutter"))
    print("dart version: ", get_version("dart"))

    print("project flutter version: ", get_project_version("flutter"))
    print("project dart version: ", get_project_version("dart"))

    print("compare versions: ", compare_versions(
        get_version("flutter"), get_project_version("flutter")))
