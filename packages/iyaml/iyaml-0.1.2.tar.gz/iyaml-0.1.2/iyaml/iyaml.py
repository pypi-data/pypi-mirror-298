import yaml
import os
import pathlib
import re
import sys
import os.path

from typing import Any, Set, Callable


class ILoader(yaml.SafeLoader):
    def __init__(self, stream):
        self._included = {str(pathlib.Path(stream.name).resolve())}
        self._dir_path = os.path.split(stream.name)[0]
        super(ILoader, self).__init__(stream)

    def load_file(self, filepath: str) -> Any:
        if filepath in self._included:
            raise ValueError("Circular inclusion detected: " + filepath)
        _, extension = os.path.splitext(filepath)
        extension = extension.lower() if not extension else extension
        with open(filepath, "r") as file:
            if extension == ".yaml" or extension == ".yml":
                return yaml.load(file, loader_wrapper(self._included))
            return file.read()

    def include(self, node):
        node_value = self.construct_scalar(node)
        filepath = os.path.join(self._dir_path, node_value)
        filepath = str(pathlib.Path(filepath).expanduser().resolve())
        res = re.search(r"^([^\*]*)(\*.*)$", filepath)
        if not res:
            return self.load_file(filepath)
        base_path = res.group(1)
        pattern = res.group(2)
        re_pattern = re.escape(
            filepath.replace('**', '*')
        ).replace('\\*', '(.*)')
        result = dict()
        for path in pathlib.Path(base_path).glob(pattern):
            if os.path.isdir(path):
                continue
            r = result
            k = None
            for p in re.search(re_pattern, str(path)).groups():
                for pp in p.split(os.sep):
                    if k is None:
                        k = pp
                    else:
                        if k not in r:
                            r[k] = dict()
                        r = r[k]
                        k = pp
            if k:
                r[k] = self.load_file(str(path))
        if not result:
            ValueError(f'Nothing included: {node_value}')
        return result

    def env(self, node):
        # TODO: raise exception if not found?
        return os.environ.get(self.construct_scalar(node), None)


ILoader.add_constructor("!include", ILoader.include)
ILoader.add_constructor("!env", ILoader.env)


def loader_wrapper(included: Set[str]) -> Callable[[Any], ILoader]:
    def wrapper(stream: Any) -> ILoader:
        result = ILoader(stream)
        result._included |= included
        return result

    return wrapper


def load(filepath: str) -> Any:
    with open(filepath) as file:
        data = yaml.load(file, ILoader)
    return data


def str_presenter(
    dumper: yaml.dumper.Dumper, data: str
) -> yaml.nodes.ScalarNode:
    """
    Makes every multiline string be a block literal.
    """
    tag = "tag:yaml.org,2002:str"
    if os.linesep in data:
        return dumper.represent_scalar(tag, data, style="|")
    return dumper.represent_scalar(tag, data)


def save(data: Any, filepath: str, **kwargs) -> None:
    yaml.add_representer(str, str_presenter)
    with open(filepath, "w") as file:
        yaml.dump(data, file, **kwargs)


def main():
    if len(sys.argv) != 2:
        print("Usage: iyaml filepath")
        exit(1)
    filepath = sys.argv[1]
    if not os.path.isfile(filepath):
        print(f'iyaml: No such file {filepath}')
        exit(2)
    data = load(filepath)
    yaml.add_representer(str, str_presenter)
    dump = yaml.dump(data)
    print(dump)
