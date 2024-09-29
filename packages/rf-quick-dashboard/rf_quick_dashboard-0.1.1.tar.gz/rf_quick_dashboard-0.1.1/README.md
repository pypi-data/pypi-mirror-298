# RF Quick Dashboard

## Overview
RF Quick Report is a tool designed to generate an HTML dashboard from JUnit test results. This dashboard provides a comprehensive view of test execution, helping you quickly identify test outcomes and trends.

## Features
- Converts JUnit XML results into an interactive HTML dashboard.
- Summarizes test results with visual charts and graphs.
- Easy to integrate with CI/CD pipelines.

## Installation
To install RF Quick Report, clone the repository and install the required dependencies:
```bash
git clone https://github.com/yourusername/RF_Quick_Report.git
cd RF_Quick_Report
pip install -r requirements.txt
```

## Usage
To generate the HTML dashboard, run the following command:
```bash
python generate_report.py --input path/to/junit/results --output path/to/output/dashboard.html
```

## Example
```bash
python generate_report.py --input ./junit_results --output ./report/dashboard.html
```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.

## Contact
For any questions or feedback, please contact [your-email@example.com](mailto:your-email@example.com).