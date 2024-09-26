# Markets Analytics Package

A utility [package](https://pypi.org/project/markets-analytics/0.1.5/#description) to that helps with data analytics by reducing boiler plate code and replacing them with helper function for database interactivity, ETL pipelines, Google Sheets, and dates.

## Installation

```sh
pip install markets_analytics
```

To install specific version of the package then run the following command:

```sh
pip install markets_analytics==X.Y.Z 
```

# Imports

The following examples showcase how to import packages for the areas you're interested in.

Although you can import original classes like `RedshiftConnector`, aliases have already been provided to reduce this step further.

Database connectivity:

```python
from markets_analytics import redshift, datalake, exasol
from markets_analytics import Redshift, Datalake, Exasol # Actual class names
```

ETL pipelines:

```python
from markets_analytics import etl
from markets_analytics import ETL # Actual class names
```

Google Sheets:

```python
from markets_analytics import GSheetHelper
gsheet = GSheetHelper('<Name of the GSheet>')
```

Date utilities:

```python
from markets_analytics import dateutil
from markets_analytics import DateUtil  # Actual class names
```

Google Chat:

```python
from markets_analytics import GoogleChat
gchat = GoogleChat('<Webhook URL of the Google Chat Space>')
```

Email

```python
from markets_analytics import Email
email = Email('<Your Email ID>', '<Your Email App Password>') # App Password is setup via Google 2FA Security tab
```

## Releasing New Version

To release new versions after making changes, we need to update the `pyproject.toml` file and increment the version's minor or major counter by 1. You would then be able to run the following in your terminal (make sure dist only contains the new version files after build command has successfully completed):

```sh
python3 -m pip install --upgrade build twine
python3 -m build
python3 -m twine upload --repository testpypi dist/* # Repository tag is optional
```

Make sure to set your twine details before uploading the package distributions:

```sh
set TWINE_USERNAME=__token__
set TWINE_PASSWORD=<pypi-token>
```
