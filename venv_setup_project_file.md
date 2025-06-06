# 🐍 Venv Setup for VS Code

This guide sets up a virtual Python environment (`venv`) for a project and links it with Visual Studio Code.

---

## ⚙️ Venv Setup

### 1. Switch to desired drive

```powershell
D:
```

### 2. Create project folder if needed

```powershell
mkdir project_file
```

### 3. Enter project folder

```powershell
cd project_file
```

### 4. Create virtual environment

```powershell
python -m venv venv
```

### 5. Activate environment (PowerShell)

```powershell
.\venv\Scripts\Activate.ps1
```

You should see the prompt change to:

```
(venv) PS D:\project_file>
```

### 6. Create VS Code interpreter settings

```powershell
mkdir .vscode
```

### 7. Create a file: `.vscode/settings.json`

Paste the following content:

```json
{
  "python.pythonPath": "D:\\project_file\\venv\\Scripts\\python.exe"
}
```

> ⚠️ Use double backslashes `\\` for valid Windows paths in JSON.

---

## 💻 How to Open Project in venv

Each time you want to work on your project:

```powershell
cd D:\project_file
.\venv\Scripts\Activate.ps1
code .
```

- `cd D:\project_file` – navigate to your project
- `Activate.ps1` – activates your virtual environment
- `code .` – opens VS Code using the environment you just activated

---

## 💻 Make a output from terminal

```powershell
cd D:/finance
python main.py --csv george.csv --output chart.html --since 2024-01-01
```

## Git repo and acc activation

```powershell
cd D:\project_file
git init
git config user.name "Ghar"
git config user.email "rudolf.tkac@seznam.cz"

```


## ✅ Ready to Code!

VS Code will now:
- Use your virtual environment
- Let you run scripts and lines using the correct Python interpreter
- Install packages inside `venv` using `pip install ...`


