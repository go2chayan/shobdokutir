# Shobdokutir
Shobdokutir is envisioned to be a comprehensive suite of natural language processing in Bengali (Bangla) and other low resource languages.

# Installation

## Using python
```
python setup.py install
```

## Docker
For the correct rendering of Bangla scripts, use the docker environment
```
docker build -t shobdokutir .
docker run -ti --name=shobdokutir shobdokutir /bin/bash
```

From within the docker environment, please execute the following command to initiate xvfb, which helps the code to render
the correct output.
```
source scripts/enable-xvfb.sh
```

# Usage
Please start by looking into the `examples.sh` for some sample usage.

# Contribution Notes
Any contribution is greatly appreciated.
Please adhere to the python style guide (http://www.itanveer.com/coding-style/) and PEP-8 standards.

* When contributing a new functionality, please try adding a command line `main` interface (check `shobdokutir.ebook.parser` for example)
* These functions demonstrate the main usage of the repository. In the future, these functions will also work as unit tests.
* Please write a sample usage of the command line interface in the `example/examples.sh`
* If the command line interface demonstration requires a sample data file, please keep it in the `resources` folder. However, avoid this dependency as much as possible to keep the repository size small.
* Please make sure the resource file size is as small as possible if at all necessary

# Contact
* Author: Md Iftekhar Tanveer
* Email:  go2chayan@gmail.com
* webpage: shobdokutir.com
