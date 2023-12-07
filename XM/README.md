# Automation Test for XM Economic Calendar

## Installation

1. Create a virtual environment:
    ```bash
    python3 -m venv venv
    ```

2. Activate the virtual environment:
- For Windows:
    ```bash
    venv\Scripts\activate.bat
    ```
- For Linux/Mac:
    ```bash
    source venv/bin/activate
    ```


3. Install required packages:
    ```bash
    pip install -r requirements.txt
    ```


## Running the tests

To run the tests, execute the following command:
```bash
   pytest tests/ --html=report.html
```
## Running the tests in parallel

To run the tests in parallel, execute the following command:
```bash
   pytest tests/ --html=report.html -v -s -n 4
```

To run tests on a different browser, provide cmd argument `--browser` with the browser name:

````bash
    pytest tests/ --browser firefox --html=report.html -v -s
    pytest tests/ --browser chrome --html=report.html -v -s
````
