# 🛡️ Mijhar - Advanced Malware Analysis Tool

![Mijhar Logo](https://raw.githubusercontent.com/kush-king249/Mijhar/main/docs/mijhar_logo.png) <!-- Placeholder for logo -->

## 📝 Project Overview

**Mijhar** is a comprehensive tool designed for analyzing malware using both Static Analysis and Dynamic Analysis techniques. This tool aims to assist cybersecurity researchers and analysts in understanding malware behavior, identifying its intentions, and extracting crucial information such as network communications, file modifications, and other suspicious indicators. The tool features two interfaces: a Command-Line Interface (CLI) for advanced users and a professional, interactive Graphical User Interface (GUI) for ease of use.

## ✨ Key Features

*   **Static Analysis:** Examines executable files without running them to extract information such as:
    *   Hashes (MD5, SHA1, SHA256).
    *   PE (Portable Executable) file information like sections, imported, and exported functions.
    *   Extraction of suspicious strings.
    *   Entropy calculation to detect encryption or packing.
    *   Searching for suspicious indicators like IP addresses, URLs, and registry keys.

*   **Dynamic Analysis:** Executes malware in an isolated environment (Sandbox) and monitors its real-time behavior, recording:
    *   Network Activity.
    *   New processes created.
    *   (Note: File and registry monitoring require an advanced sandbox environment or additional tools).

*   **Risk Assessment:** A system to evaluate the severity level of malware based on indicators detected in both analysis types.

*   **Comprehensive Reports:** Generates detailed and clear reports in multiple formats (HTML, JSON, Text) for analysis results.

*   **Command-Line Interface (CLI):** A powerful and flexible tool for analysts who prefer command-line interaction.

*   **Graphical User Interface (GUI):** An attractive, interactive, and user-friendly web interface, built using Flask and HTML/CSS/JavaScript, allowing file uploads and visual display of analysis results.

## 🚀 Quick Start

### Prerequisites

Ensure you have Python 3.x and `pip` installed on your system.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/kush-king249/Mijhar.git
    cd Mijhar
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Linux/macOS
    # venv\Scripts\activate  # For Windows
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

    *Note:* You might need to install additional development packages for your system to compile `yara-python` and `pefile` correctly. On Debian/Ubuntu systems, you might need:
    ```bash
    sudo apt-get update
    sudo apt-get install -y build-essential python3-dev libssl-dev
    ```

### Usage

#### 🌐 Web GUI

To run the web interface, use the following command:

```bash
python3 run.py web
```

After running, open your web browser and navigate to `http://localhost:5000`.

#### 💻 Command-Line Interface (CLI)

You can use the CLI to analyze files directly. Here are some examples:

*   **Show help:**
    ```bash
    python3 run.py cli --help
    ```

*   **Show tool information:**
    ```bash
    python3 run.py cli info
    ```

*   **Static analysis of a file:**
    ```bash
    python3 run.py cli static <file_path> -o static_report.json -f json -v
    ```

*   **Dynamic analysis of a file:**
    ```bash
    python3 run.py cli dynamic <file_path> -o dynamic_report.json -f json -v -t 30
    ```

*   **Comprehensive analysis (static and dynamic) of a file and generate an HTML report:**
    ```bash
    python3 run.py cli analyze <file_path> -o combined_report.html -f html -v -t 60
    ```

*   **View a saved report:**
    ```bash
    python3 run.py cli view <report_path.html>
    ```

## 📸 Screenshots

<!-- Screenshots of the GUI will be added here later -->

## 🤝 Contributing

Contributions are welcome to improve the Mijhar tool. Please read `CONTRIBUTING.md` (to be added later) for guidelines.

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file (to be added later) for more details.

## 👨‍💻 Author

**Hassan Mohamed Hassan Ahmed**

*   GitHub: [kush-king249](https://github.com/kush-king249)

---
