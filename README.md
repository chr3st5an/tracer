<div align="center">

[![Logo](https://i.imgur.com/HV5KtwO.png)](https://github.com/chr3st5an/tracer)

[![Maintainer](https://img.shields.io/badge/Maintainer-chr3st5an-cyan.svg)](https://github.com/chr3st5an)
[![Python](https://img.shields.io/badge/Python->=3.7-yellow.svg)](https://www.python.org/downloads/release/python-3712/)
[![GitHub license](https://badgen.net/github/license/Naereen/Strapdown.js)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)
![Open Source](https://badgen.net/badge/Open%20Source/Yes/blue?icon=github)
![Version](https://img.shields.io/badge/Version-1.0.2-blue.svg)

Tracer is an OSINT tool that can be used to detect on which websites a username is currently in use.

</div>

[![Tracer - Preview](https://i.imgur.com/QTtt9oZ.jpg)](https://github.com/chr3st5an/tracer)

---

## 💡 Features

Tracer provides the following features:

- 170+ sites that are checked

- Filter websites based on their domain or category

  - Limit the pool of sites that will be checked

- Browser version (GUI)

- Save the result of each check in a report file

- Open successful results in your browser

- Customizability:

  - Use the included config file to change the behavior of Tracer

- Easy to use

---

## 📥 Installation

```bash
git clone https://github.com/chr3st5an/tracer.git
```

> 🛈 If you do not have `git`, you can download this repository by clicking on `Code` > `Download ZIP`. Unzip the folder and open a terminal.

```bash
cd tracer/
```

```bash
python -m pip install -r ./requirements.txt
```

> 🛈 Your OS might be equipped with the `python3` and `pip3` commands instead of `python` and `pip`
---

## 🔨 Usage

```bash
python tracer/ [OPTIONS] username  # Executing the folder
```

```bash
python tracer.py [OPTIONS] username  # Executing the script
```

---

## 🍿 Using Tracer in your browser

```bash
python tracer/ --web tracer
```

Runs a local server on port 12345 which automatically gets opened in your browser

---

## 👀 All options

For a list of all options run the following command

```bash
python tracer.py --help
```

</br></br>

<div align="center">

![Made With Python](https://ForTheBadge.com/images/badges/made-with-python.svg)

</div>
