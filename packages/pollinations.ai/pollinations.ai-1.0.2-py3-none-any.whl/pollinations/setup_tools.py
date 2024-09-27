import subprocess
import os

commands: list = [
  #"cd pollinationsv2",
  #"python setup.py sdist bdist_wheel",
  #"twine upload dist/*",
  #str(os.getenv("pypi-api-key"))
]

def build(*args, **kwargs) -> None:
  for command in commands:
    subprocess.run(command, shell=True)