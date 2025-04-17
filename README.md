## 🛠️ DamCrawler by DamClover

A powerful Python utility that crawls and extracts unique GET parameters from URLs using `gau` and `katana`, with support for filters like extensions, keywords, silent mode, directory finder, and anothers.  

### 📦 Requirements

- **Python 3.6+**
- **Go (for `gau` and `katana`)**

### 🔧 Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/damclover/damcrawler
cd damcrawler
```

#### 2. Install gau and katana 

Run the installer script for gau and put the damcrawler global:

```bash
sudo chmod +x install.sh
./install.sh
```

⚠️ This script installs gau and katana via Go and adds it to your PATH. Make sure Go is installed.

#### 3. Install Python Requirements

```bash
pip3 install -r requirements.txt
```

---

### 🚀 Usage

```bash
DamCrawler -u https://example.com/
```

#### 🔹 Save output to a file:

```bash
DamCrawler -u https://example.com/ -o params.txt
```

#### 🔹 Global use:

```bash
DamCrawler -u https://example.com/ -fc
```
⚠️ This script parameter will extract all possible URLs from the target, possibly revealing hidden directories or files.

#### 🔹 Show Help for more options:

```bash
DamCrawler -h
```

---

### 📥 Example Output

```bash
https://example.com/page.php?id=
https://example.com/view.php?item=
https://example.com/search.php?q=
```

---
# Att
* Added a variety of payloads and wordlists
* Automation of the katana tool

---

## 🧑‍💻 Author

DamClover  
For educational and testing purposes only.
