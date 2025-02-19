# Log File Analyzer

## Overview
This Python application reads a log file in CSV format, analyzes the log data, and generates an output CSV file (`output.csv`). The application categorizes tasks based on their execution time:
- Tasks that take **more than 10 minutes** are marked as **errors**.
- Tasks that take **between 5 and 10 minutes** are marked as **warnings**.

## Features
- Reads and processes log data from a CSV file
- Analyzes task execution times
- Generates an output CSV file (`output.csv`) with categorized results

## Installation
1. Clone this repository:
   ```sh
   git clone <repository-url>
   cd log-file-analyzer
   ```
2. Install required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
Run docker-compose
```bash
./docker.sh
```
Run the script with:
```bash
python main.py input_log.csv
```
Replace `input_log.csv` with the actual log file you want to analyze.

## Run Test
Run all tests
```bash
pytest
```

Run a specific directory
```bash
pytest tests/
```

Run tests with coverage
```bash
pytest --cov
```

## Troble shooting
If you experince error `permission denied`, you can fix by run
```bash
chmod +x ./docker.sh
```

  ## Output
The generated `output.csv` file will contain the analyzed results with task execution times classified as **error**, **warning**, or **normal**.


## How to build docker image

```bash
# Build docker file
docker build -t log-monitoring .

# Run docker bash
docker run --rm -it log-monitoring bash
```

## License
This project is open-source and available for modification and distribution.

