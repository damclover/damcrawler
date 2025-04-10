---

## 🛠️ ParamFinder by DamClover

A simple Python utility that extracts unique GET parameters from `.php?` URLs using `gau`.

---

### 📦 Requirements

- **Python 3.6+**
- **Go (for `gau`)**

---

### 🔧 Installation

#### 1. Clone the Repository (if needed)
```bash
git clone https://github.com/yourusername/paramfinder.git
cd paramfinder
```

#### 2. Install `gau`
Run the helper script:

```bash
bash install-gau.sh
```

This will install `gau` via Go and add it to your `PATH` automatically.

> ⚠️ Requires Go installed on your system.

#### 3. Install Python Requirements
Make sure you have Python 3, then install the dependencies:

```bash
pip3 install -r requirements.txt
```

---

### 🚀 Usage

```bash
python3 paramfinder.py -u https://example.com/
```

#### Optional:
- Save output to file:
```bash
python3 paramfinder.py -u https://example.com/ -o params.txt
```

- Specify the param
```bash
python3 paramfinder.py -u <url> [-p <param1,param2>]
python3 paramfinder.py -u <url> -p id,page
```

- Show help:
```bash
python3 paramfinder.py -h
```

---

### 📥 Example Output

```
https://example.com/page.php?id=
https://example.com/view.php?item=
https://example.com/search.php?q=
```

### Bonus!!!
- To transform it into a global tool, being executed from anywhere
```bash
chmod +x paramfinder.py
sudo cp paramfinder.py /usr/local/bin/paramfinder
```

---

### 🧑‍💻 Author

**DamClover**  
For educational and testing purposes only.

---
