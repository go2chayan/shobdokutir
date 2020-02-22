# Shobdokutir

Shobdokutir is envisioned to be a comprehensive suite for natural language processing in Bengali (Bangla) and other low resource languages.

Any contribution is greatly appreciated.
Please adhere to the python styleguide (http://www.itanveer.com/coding-style/) and PEP-8 standards.

# Installation

## Using python
```
python setup.py install
```

## Docker
For the correct rendering of Bangla scripts, use the docker environment
```
docker build -t shobdokutir .
docker run -ti --name shobdokutir shobdokutir /bin/bash
```

From within the docker environment, please execute the following command to initiate xvfb, which helps the code to render
the correct output.
```
source scripts/enable-xvfb.sh
```

# Contact
* Author: Md Iftekhar Tanveer
* Email:  go2chayan@gmail.com
* webpage: shobdokutir.com
