# appodeal_py

AppoDeal API Client library for Python.

## Installation

```bash
$ pip install git+https://github.com/PoradaKev/appodeal_py
```

## Usage

```python
from appodeal import Appodeal

api_token = "b51dd49e89bae7e3fa646ec5e1c7082d"
user_id = 102910

ap = Appodeal(api_token, user_id)

date_from = "2020-06-18"
date_to = "2020-06-20"

appodeal_df = ap.report(date_from=date_from, date_to=date_to)

print(appodeal_df)
```

## License

MIT

## Author

[Oleksandr Korshun](https://github.com/PoradaKev)
