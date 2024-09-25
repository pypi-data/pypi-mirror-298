# iYAML

iYAML is a YAML macro processor.

iYAML provides the following YAML tags:
- `!include` - to include the content of the specified file, or
   files matching the given wildcard
- `!env` - to include the value of the specified environment variable


# Installation

Install default version from the
[Python Package Index](https://pypi.org/project/iyaml/):

```
pip install iyaml
```


# Examples

Here is an example of including files and environment variables:
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

