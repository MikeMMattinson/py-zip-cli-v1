#!/bin/bash

ROOT="/mnt/veracrypt1"

declare -A FOLDERS

# Define folder paths and README content
FOLDERS["Personal_ID"]="Folder: Personal_ID
Description: Contains scanned copies of personal identity documents for all household members.

Examples:
- Driver's Licenses
- Passports
- State IDs

Ensure all documents are current and legible.
"

FOLDERS["Legal_Documents"]="Folder: Legal_Documents
Description: Legal records, certifications, and personally identifying paperwork.

Subfolders:
- Birth_Certificates: Scanned originals for all household members
- Wills_and_POA: Last will, Power of Attorney, Advanced Directives
- Social_Security_Cards: Scanned social security cards (USA only)

Update regularly with most recent signed copies.
"
FOLDERS["Legal_Documents/Birth_Certificates"]=""
FOLDERS["Legal_Documents/Wills_and_POA"]=""
FOLDERS["Legal_Documents/Social_Security_Cards"]=""

FOLDERS["Insurance"]="Folder: Insurance
Description: Current insurance policy documents for health, auto, and home.

Subfolders:
- Medical: Health insurance cards, policies, emergency instructions
- Auto: Car/truck insurance policies and claim instructions
- Homeowners_Renters: Property insurance and policy contact info

Keep policy numbers, expiration dates, and contact info up to date.
"
FOLDERS["Insurance/Medical"]=""
FOLDERS["Insurance/Auto"]=""
FOLDERS["Insurance/Homeowners_Renters"]=""

FOLDERS["Emergency_Info"]="Folder: Emergency_Info
Description: Quick reference files for emergencies, travel, or healthcare events.

Include:
- Emergency contacts (family, doctor, lawyer)
- Known medical conditions, allergies, medications
- Blood types and health directives

Keep a printed version of this file in your grab bag if possible.
"

FOLDERS["Travel_Docs"]="Folder: Travel_Docs
Description: Travel-related documentation and scanned visa records.

Subfolders:
- Visa_Records: Country-specific visa documents, entrance permits

Also include:
- COVID vaccination cards or international health certificates
- Any travel medical insurance PDFs
"
FOLDERS["Travel_Docs/Visa_Records"]=""

# Create folders and README files
for folder in "${!FOLDERS[@]}"; do
    fullpath="$ROOT/$folder"
    mkdir -p "$fullpath"
    if [[ -n "${FOLDERS[$folder]}" ]]; then
        echo "${FOLDERS[$folder]}" > "$fullpath/README.txt"
    fi
done

echo "[OK] Folder tree and README files created at $ROOT"
