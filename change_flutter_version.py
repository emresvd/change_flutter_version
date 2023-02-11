import os


def get_version(tool: str) -> str:
    output = os.popen('flutter --version').read()
    return output.split()[output.split().index(tool) + 1]


def get_project_version(tool: str) -> str:
    tool += ":"

    with open("pubspec.lock", "r", encoding="utf-8") as f:
        data = f.read()
    
    sdks = False
    for line in data.splitlines():
        if line.strip() == "sdks:":
            sdks = True
        if sdks and line.strip().startswith(tool):
            return line.replace(tool, "").strip().strip('"')


if __name__ == '__main__':
    print("flutter version: ", get_version("Flutter"))
    print("dart version: ", get_version("Dart"))

    print("project flutter version: ", get_project_version("flutter"))
    print("project dart version: ", get_project_version("dart"))
