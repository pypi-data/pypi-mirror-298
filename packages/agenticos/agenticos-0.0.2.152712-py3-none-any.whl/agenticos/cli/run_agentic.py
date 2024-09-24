from subprocess import run


def run_agentic(mode: str, port: int, dev: bool) -> None:
    if mode == "httpserver":
        cmd = ["fastapi"]
        cmd += ["dev", "--reload"] if dev else ["run"]
        cmd += ["--port", str(port)]
        cmd += ["src/agentic/agentic_node.py"]
        print("Running command: ", cmd)
        run(cmd, check=True)
    else:
        raise ValueError("Invalid mode")
