from setuptools import setup
from tm import tm

setup(name="tm",
      version=tm.__version__,
      url="https://github.com/Ethanal/tm",
      license="MIT",
      packages=["tm"],
      entry_points = {
          "console_scripts": [
              "tm = tm.tm:main",
          ],
      },
      long_description=tm.__description__)