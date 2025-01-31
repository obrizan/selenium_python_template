# Selenium + Python Template Project

Welcome to the Selenium + Python Template Project! This repository provides a well-structured, scalable framework for test automation using Selenium WebDriver and Python. It's designed to help you get started quickly and maintain your test automation efforts efficiently.

## 📋 Features

- **Modular Design**: Organized structure with reusable components like PageObjects and Test Data Factories.
- **Scalability**: Easy to extend for larger projects.
- **Integration-Ready**: Built-in support for integrating with APIs, CI/CD pipelines, and reporting tools.
- **Cross-Browser Support**: Pre-configured WebDriver factory for managing multiple browsers.
- **Auto-waiting**: `WebDriver.click()` waits for an element to be clickable automatically.

## 🏗️ Project Structure

```plaintext
selenium_python_template/
├── .github/workflows/ui-tests.yml      # GitHub Workflow
├── pages/                              # PageObject classes
├── tests/                              # Test scripts
├── utils/                              # Utility functions (e.g. text processing)
├── data/                               # Test data files (coming soon)
├── test-reports/                       # Test execution reports
├── drivers/                            # WebDriver binaries (optional)
├── config/                             # Configuration files (coming soon)
├── requirements.txt                    # Python dependencies
├── bitbucket-pipelines.yml             # BitBucket Pipelines configuration
└── conftest.py                         # Global fixtures
```

## 🚀 Getting Started

### Prerequisites

* Python 3.9+
* Google Chrome or Firefox or Safari to run & debug tests locally
* pip (Python package installer)

### Installation

Download the Selenium Python Template project from releases page: [https://github.
com/obrizan/selenium_python_template/releases/](https://github.com/obrizan/selenium_python_template/releases/).

Create and activate virtual environment (optional, but recommended):

```bash
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set up WebDriver (optionally):

Download the appropriate WebDriver for your browser (ChromeDriver, GeckoDriver, etc.)
Place it in the drivers/ directory or update your system PATH.

## ⚙️Configuration

Set environment variables. Pay attention to `FRONTEND_URL` — it doesn't have any default value, it must be set 
before running tests.

| Variable             | Description                                                             | Default                |
|----------------------|-------------------------------------------------------------------------|------------------------|
| `FRONTEND_URL` | Base URL for web application under test.                                |                        |
| `SELENIUM_DRIVER_KIND` | Options: `remote`, `chrome`, `safari`, `firefox`.                       | `chrome`               |
| `REMOTE_DRIVER_URL` | Used when `SELENIUM_DRIVER_KIND=remote`.                                | `http://localhost:3000` |
| `WINDOW_RESOLUTION` | Browser window resolution. Values are defined in `webdriver_factory.py` | `DESKTOP_1280X720`     |

## 🧪 Running Tests
Run all tests using pytest:

```bash
pytest --html=test-reports/report.html --self-contained-html
```

Specify a particular test file or function:

```bash
pytest tests/test_example.py
```

## 🛠️ Customization

* **Adding Pages:** Create new classes in pages/ to represent additional pages or components.
* **Adding Tests:** Write test scripts in tests/ and use the pytest framework for execution.
* **Configuration:** Update config/ files to customize browser, test data paths, and other settings.

## 📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

## 🙌 Contributing
Contributions are welcome! If you'd like to improve this project, feel free to fork the repository and submit a pull request.

## 📞 Contact
Have questions or suggestions? Reach out:

**Author:** Volodymyr Obrizan

**Email:** volodymyr.obrizan@gmail.com

Happy Testing! 🚀
