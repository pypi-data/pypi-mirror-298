This project is intended to be used as a type _hinting_ system for a related project, `practical_astronomy`.

It felt plausible that it would be useful in other projects as well, so it has been spun off into an indepdenent file.

# Install

`pip install astronomy-types`

`import astronomy_types`

# Updating and Repackaging the Project with `setuptools`

To update and repackage this Python project using `setuptools` on macOS, follow these steps:

## 1. Install or Activate the Virtual Environment

It's recommended to use a virtual environment for isolation. If you don't already have a virtual environment, create and activate one:

### a. Create a virtual environment:

```bash
python3 -m venv venv
```

### b. Activate the virtual environment:

```bash
source venv/bin/activate
```

## 2. Install Required Dependencies

Ensure that setuptools and wheel are installed in your environment:

```bash
pip install setuptools wheel twine
```

or

```bash
pip install -r requirements.txt
```

## 3. Update version number

```bash
setup(
    name="my_project",
    version="0.2.0",  # Update this to the new version number
    ...
)
```

## 4. Build the dist

```bash
python3 setup.py sdist bdist_wheel
```

## 5. Upload with `twine`

```bash
twine upload dist/*
```

And enter in the API token
