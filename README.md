# Code names service

### Description:
Docs: /docs

### Setting up:
1. Put 'serviceAccount.json' to src/firebase/
2. Create python [virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/):
    - Linux `virtualenv {name}`
    - Windows `py -m venv {name}`
3. Activate environment:
    - Linux `source {name}/bin/activate`
    - Windows `{name}\Scripts\activate.bat` 
4. `pip install -r requirements.txt`

### Start:
`python -m uvicorn src.main:app --reload --port 8083`


