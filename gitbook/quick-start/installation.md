---
description: >-
  An installation procedure for those who want to contribute to the development
  of IGS2.
---

# Dev install

## 1. Clone the IGS2 GitHub repo

Clone the IGS2 GitHub repository to a local folder.

{% embed url="https://github.com/BlockResearchGroup/compas-IGS2" %}

## **2. Create a dev environment**

Use `conda` to create a development environment, for example "igs2-dev", and install `python-planarity`, and `cython`.

```
conda config --add channels conda-forge
conda create -n igs2-dev python=3.9 python-planarity cython
```

## 3. Install IGS2 from a local repo

In the dev environment, use pip to install an editable, local version of IGS2.

Activate the IGS2 environment, then go to the root directory of IGS2:

```
conda activate igs-dev
cd path/to/local/compas-IGS2
```

Install IGS2:

```
pip install -e .
```

## 4. Install IGS2 plugin to Rhino

<pre><code><strong>python -m compas_rhino.install -v 7.0 --clean
</strong></code></pre>
