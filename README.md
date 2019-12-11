# vertical-cooperative
This repository gather odoo modules for cooperatives

## Installation with pip

We used [odoo setup tools](https://pypi.org/project/setuptools-odoo/#packaging-a-single-addon) to generate the pypi files from the odoo manifests. To install all modules, first create a venv with this name (it's git-ignored)
```shell
python -m venv venv
```
And then use the testing requirements file:

```shell
pip install -r requirements_only_for_testing.txt
```
If one fails but you want to try also the next ones, you can read each line separately:

```bash
while read MODULE
do
  pip install $MODULE
done < requirements_only_for_testing.txt
```
