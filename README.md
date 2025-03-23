# Arcsploit v1.0

Arcsploit is a powerful security tool designed for penetration testing and vulnerability assessment. The current version includes a vulnerability scanner and a directory buster, making it easier for security professionals to identify potential weaknesses in web applications.

## Features v1.0

- **Vulnerability Scanner**: Automatically scans web applications for known vulnerabilities.
- **Directory Buster**: Identifies hidden directories and files on web servers.

## Installation

To get started with Arcsploit, you'll need to install the required dependencies. Follow the steps below:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/arcsploit.git
   cd arcsploit
   ```
2.Create a virtual environment:

   ```bash
   python3 -m venv venv
   ```
   Activate the virtual environment:
   On Windows:
   ```bash
   venv\Scripts\activate
   ```
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```
3. Install the required packages using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the vulnerability scanner or directory buster, use the following command:

```bash
python3 arcsploit.py
```

Make sure to replace `arcsploit.py` with the actual name of your main Python file if it's different.

## Legal Disclaimer

**Arcsploit** is intended for educational purposes and ethical hacking only. By using this tool, you agree to comply with all applicable laws and regulations. Unauthorized use of this tool against systems you do not own or have explicit permission to test is illegal and may result in severe penalties.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Feel free to contribute to the project or report any issues you encounter. Happy hacking!
