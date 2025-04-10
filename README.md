## 🛠️ DamCrawler by DamClover

A powerful Python utility that crawls and extracts unique GET parameters from URLs using `gau`, with support for filters like extensions, keywords, silent mode, and more.  
It also supports extracting pages by title keywords such as `login`, `admin`, etc.

### 📦 Requirements

- **Python 3.6+**
- **Go (for `gau`)**

### 🔧 Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/damcrawler.git
cd damcrawler
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

---

### 🚀 Usage

```bash
DamCrawler -u https://example.com/
```

#### 🔹 Save output to a file:

```bash
DamCrawler -u https://example.com/ -o params.txt
```

#### 🔹 Filter by specific parameters:

```bash
DamCrawler -u https://example.com/ -p id,page
```

#### 🔹 Show only `.php` files **without parameters**:

```bash
DamCrawler -u https://example.com/ -np
```

#### 🔹 Filter by file extensions:

```bash
DamCrawler -u https://example.com/ -f php,html
```

#### 🔹 Search for keywords in URLs:

```bash
DamCrawler -u https://example.com/ -kw upload,admin,files
```

#### 🔹 Silent Mode (only shows scanning message):

```bash
DamCrawler -u https://example.com/ -s
```

#### 🔹 Search by page `<title>`:

```bash
DamCrawler -u https://example.com/ -t admin,login
```

#### 🔹 Show Help:

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

## 🎁 Bonus: Make it Global

To run `DamCrawler` from anywhere:

```bash
chmod +x DamCrawler
sudo mv DamCrawler /usr/local/bin/
```

✅ Now you can use it like this:

```bash
DamCrawler -u https://example.com/
```

---

## 🧑‍💻 Author

DamClover  
For educational and testing purposes only.
