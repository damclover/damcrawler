## 🛠️ DamCrawler by DamClover

A powerful Python utility that crawls and extracts unique GET parameters from URLs using `gau`, with support for filters like extensions, keywords, silent mode, and more.  
It also supports extracting pages by title keywords such as `login`, `admin`, etc.

### 📦 Requirements

- **Python 3.6+**
- **Go (for `gau`)**

### 🔧 Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/damcrawler
cd damcrawler
```

#### 2. Install gau and /usr/local/bin/

Run the installer script for gau and put the damcrawler global:

```bash
bash install.sh
```

⚠️ This script installs gau via Go and adds it to your PATH. Make sure Go is installed.

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
DamCrawler -u https://example.com/ -gs
```

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

## 🧑‍💻 Author

DamClover  
For educational and testing purposes only.
