
from pathlib import Path
import re
import shutil

# Folder containing your 100 HTML articles
SITE_DIR = Path(__file__).parent

# Navbar HTML
NAVBAR = """
<!-- COMMON NAVBAR START -->
<nav class="common-navbar">
    <div class="navbar-logo">Windows Helpdesk</div>

    <div class="navbar-buttons">
        <button type="button">Home</button>
        <button type="button">Toll Free No.</button>
        <button type="button">Login Now</button>
        <button type="button">Support Now</button>
    </div>
</nav>
<!-- COMMON NAVBAR END -->
"""

# Navbar CSS
CSS = """
<style id="common-navbar-style">
.common-navbar {
    width: 100%;
    min-height: 70px;
    background: #101d36;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 5%;
    box-sizing: border-box;
    font-family: Arial, sans-serif;
    flex-wrap: wrap;
    gap: 12px;
}

.navbar-logo {
    color: white;
    font-size: 22px;
    font-weight: bold;
}

.navbar-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.navbar-buttons button {
    background: #1677ff;
    color: white;
    border: none;
    padding: 11px 17px;
    border-radius: 7px;
    font-size: 14px;
    font-weight: bold;
    cursor: pointer;
}

.navbar-buttons button:hover {
    background: #0056c7;
    transform: translateY(-2px);
}

@media (max-width: 600px) {
    .common-navbar {
        flex-direction: column;
        align-items: center;
    }

    .navbar-buttons {
        justify-content: center;
    }
}
</style>
"""

# Backup folder
BACKUP_DIR = SITE_DIR / "navbar_backups"
BACKUP_DIR.mkdir(exist_ok=True)

updated = 0
skipped = 0

# Find all HTML files, excluding backups
for file in SITE_DIR.rglob("*.html"):

    if BACKUP_DIR in file.parents:
        continue

    html = file.read_text(encoding="utf-8")

    # Avoid duplicate navbar
    if "COMMON NAVBAR START" in html:
        skipped += 1
        continue

    # Create backup
    backup_path = BACKUP_DIR / file.relative_to(SITE_DIR)
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(file, backup_path)

    # Add CSS inside head
    if re.search(r"</head\s*>", html, re.I):
        html = re.sub(
            r"</head\s*>",
            lambda m: CSS + "\n" + m.group(0),
            html,
            count=1,
            flags=re.I
        )
    else:
        html = CSS + html

    # Add navbar immediately after body
    if re.search(r"<body\b[^>]*>", html, re.I):
        html = re.sub(
            r"<body\b[^>]*>",
            lambda m: m.group(0) + "\n" + NAVBAR,
            html,
            count=1,
            flags=re.I
        )
    else:
        html = NAVBAR + html

    file.write_text(html, encoding="utf-8")
    updated += 1

print("Navbar installation completed!")
print("Articles updated:", updated)
print("Already having navbar:", skipped)
print("Backups saved in:", BACKUP_DIR)
