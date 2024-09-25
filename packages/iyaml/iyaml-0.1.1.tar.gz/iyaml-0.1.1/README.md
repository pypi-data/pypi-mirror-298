# iYAML

iYAML is a Python module that allows you to insert the content of the specified
file or files into the original YAML file. This is usefull to split a large
YAML file into multiple files to imporove readability and ease of maintenance.
iYAML can also include values from environment variables.

iYAML provides the following YAML tags:
- `!include` - to include the content of the specified file, or
   files matching the given wildcard
- `!env` - to include the value of the specified environment variable

iYAML stands for "includable YAML".


# Installation

Install default version from the
[Python Package Index](https://pypi.org/project/iyaml/):

```
pip install iyaml
```


# Examples

Here is a YAML file:
```yaml
foo:
  greeting: !include greeting.txt
  secret_token: !env TOKEN

bar: !include temlates/*.sql
```

To load the YAML file use the following code:
```python
import iyaml


data = iyaml.load("file.yaml")
```

