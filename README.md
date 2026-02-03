# Snyk Target Cleanup Tool

[![Snyk](https://img.shields.io/badge/Snyk-REST%20API-700178)](https://docs.snyk.io/snyk-api)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)

A utility script to programmatically list your Snyk Organizations and bulk-delete all targets (repositories, container images, etc.) within a selected organization.

## ⚠️ High Risk: Irreversible Action
**This script performs destructive actions.** Deleting a target in Snyk permanently removes:
* All associated projects within that target.
* Historical scan data and snapshots.
* Pending fix advice.

**This cannot be undone.** Always use the `--dry-run` flag first.

---

## 🛠 Features
- **Interactive Org Selection:** Automatically fetches and lists all Organizations you have access to.
- **Smart Pagination:** Handles large environments by automatically fetching all pages of targets.
- **Dry Run Mode:** Preview deletions without making actual API calls.
- **Safety Confirmation:** Requires explicit `yes` input before proceeding with deletions.

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python 3.8+**
- A **Snyk API Token** (found in your [Snyk Account Settings](https://app.snyk.io/account)).

### 2. Installation
Clone this repository or download the script, then install the required dependencies:

`pip install -r requirements.txt`

### 3. Environment Setup
The script authenticates using the `SNYK_TOKEN` environment variable.

**macOS / Linux:**
`export SNYK_TOKEN="your-snyk-api-token"`

**Windows (PowerShell):**
`$env:SNYK_TOKEN="your-snyk-api-token"`

---

## 📖 Usage

### Standard Mode
Run the script and follow the on-screen prompts to select an organization and confirm deletion.

`python snyk-delete-targets.py`

### Dry Run Mode (Recommended)
Use this flag to see what *would* happen without actually deleting anything.

`python snyk-delete-targets.py --dry-run`

---

## 📝 How it Works
1. **Fetch Orgs:** The script calls the `/orgs` endpoint to give you a menu of choices.
2. **Fetch Targets:** It gathers every target ID in the selected organization using pagination to ensure no data is missed.
3. **Delete:** If confirmed (and not in dry-run mode), it iterates through the list, sending a `DELETE` request for each target ID.

## 📄 License
This tool is provided "as is" without warranty of any kind. Use at your own risk.
