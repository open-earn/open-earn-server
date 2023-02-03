from __future__ import print_function
from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape
from src.external import sum
import inspect

env = Environment(
    loader=PackageLoader("src", "templates"),
    autoescape=select_autoescape(["py"]),
)
template = env.get_template("generated.txt")
source_code = inspect.getsource(sum)
generated_code = template.render(source_code=source_code)
Path(__file__).parent.joinpath("./src/generated.py").write_text(generated_code)

from src.generated import AImpl

print(AImpl().sum(1, 2))
