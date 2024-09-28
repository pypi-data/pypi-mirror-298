import toml


def load_toml(file_name: str):
    with open(file_name) as file:
        return toml.load(file)


worker_envs = load_toml("workspace/worker.toml")
