## 🛠️ ParamFinder by DamClover

A simple Python utility that extracts unique GET parameters from `.php?` URLs using `gau`, with filters for specific params, extensions, keywords, and more.

### 📦 Requirements

- **Python 3.6+**
- **Go (for `gau`)**

### 🔧 Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/paramfinder.git
cd paramfinder
```
#### 2. Install gau

Run the helper script:

```bash
bash install-gau.sh
```
⚠️ This script installs gau via Go and adds it to your PATH. Make sure Go is installed.

#### 3. Install Python Requirements

```bash
pip3 install -r requirements.txt
```

### 🚀 Usage

```bash
python3 paramfinder.py -u https://example.com/
```

🔹 Save output to a file:
´´´bash
python3 paramfinder.py -u https://example.com/ -o params.txt
´´´

🔹 Filter by specific parameters:
´´´bash
python3 paramfinder.py -u https://example.com/ -p id,page
´´´

🔹 Show only .php files without parameters:
´´´bash
python3 paramfinder.py -u https://example.com/ -np
´´´

🔹 Filter by file extensions:
´´´bash
python3 paramfinder.py -u https://example.com/ -f php,html
´´´

🔹 Search for keywords in URLs:
´´´bash
python3 paramfinder.py -u https://example.com/ -kw upload,admin,files
´´´

🔹 Silent Mode (only shows scanning message):
´´´bash
python3 paramfinder.py -u https://example.com/ -s
´´´

🔹 Show Help:
´´´bash
python3 paramfinder.py -h
´´´

### 📥 Example Output
´´´bash
https://example.com/page.php?id=
https://example.com/view.php?item=
https://example.com/search.php?q=
´´´

## 🎁 Bonus

Make it a global command:
´´´bash
chmod +x paramfinder.py
sudo cp paramfinder.py /usr/local/bin/paramfinder
´´´

##### Now you can use it like this:
´´´bash
paramfinder -u https://example.com/
´´´

##🧑‍💻 Author
´´´bash
DamClover
For educational and testing purposes only.
´´´
