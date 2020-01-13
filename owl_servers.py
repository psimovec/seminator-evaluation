import subprocess


def get_ldba_pipeline(acc="gba", mode="symmetric"):
    if  acc == "gba":
        tool = "ltl2ldgba"
    elif acc == "ba":
        tool = "ltl2ldba"
    else:
        raise ValueError(f"acc should be \"gba\" or \"ba\".\n{acc} given")

    if mode not in ["symmetric","asymmetric","a","s"]:
        raise ValueError(f"Mode has to be `s` or `a`. {mode} given")
    mode = f"-{mode}" if len(mode) == 1 else f"--{mode}"
    return f"ltl --- simplify-ltl --- {tool} {mode} --- hoa"


def get_all_ldba_pipelines():
    return {f"owl#{acc}#{mode}" : get_ldba_pipeline(acc, mode) \
            for acc in ["ba", "gba"] for mode in ["a", "s"]}


class OwlServerManager():
    """Manages owl servers.
    """

    def __init__(self, start_port=6060):
        self.next_port = start_port
        self.servers = {}
        self.processes = {}

    def new_server(self, name, pipeline, port=None):
        """Run new owl server for given `pipeline`

        Returns port of the created server
        """
        if port is None:
            port = self.next_port
            self.next_port += 1

        self.servers[name] = port

        args = ["owl-server","--port", str(port)] + pipeline.split()
        proc = subprocess.Popen(args)
        self.processes[port] = proc
        return port

    def terminate_server(self, port):
        """Terminate server for listening on given `port`."""
        proc = self.processes.pop(port, None)
        if proc is None:
            raise ValueError(f"Server for port {port} does not exists."
                             "It might have been closed already."
                             )
        proc.terminate()

    def terminate_all(self):
        """Terminate all servers"""
        for port, proc in self.processes.items():
            proc.terminate()
        self.processes = {}

    def get_client_cmd(self, name):
        port = self.servers[name]
        return f"owl-client localhost {port} %f"

    def get_clients(self):
        d = {}
        for name in self.servers:
            d[name] = self.get_client_cmd(name)
        return d

    def print_ports(self, file=None):
        """Return all client commands

        format (one cmd per line):
        name:port
        """
        lines = []
        for name, port in self.servers.items():
            lines.append(f"{name}:{port}")

        if file is not None:
            print("\n".join(lines), file=file)

        return "\n".join(lines)

    def load_ports_from_file(self, filename):
        """Loads ports from file

        Loaded servers cannot be terminated
        """
        lines = open(filename, "r").readlines()
        for line in lines:
            name, port = line.split(":")
            self.servers[name] = port.rstrip()