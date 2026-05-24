---
name: theduylifeos-filing
description: Sort loose files (Downloads, new docs) into the user's theduylifeos filing system at /Users/theduy/theduylifeos/.
---

# theduylifeos Filing System

Map files from Downloads or other loose locations into the user's structured filing system at `/Users/theduy/theduylifeos/`.

## Trigger conditions
- User asks to organize, sort, or clean up Downloads, Desktop, or other loose-file locations
- User downloads a document and asks where to file it
- User wants to batch-sort new files into their existing structure

## Folder Structure

```
/Users/theduy/theduylifeos/
├── Archive/              # Old Business, Education, Finance, Personal, Projects
├── Business HoldCo/      # Holding companies
│   ├── 9444-7422 Quebec Inc. (50% Maily)
│   ├── 9496-1075 Québec inc (50% Charlesbourg)
│   ├── 9521-8749 Québec (takeover Ongles Quebec)
│   └── LAVIESTELLA
├── Business OptCo/       # Operating companies
│   ├── CHARLESBOURG/
│   ├── MAILY/
│   ├── RIVIERES/
│   └── SS/               # Sans Souci
├── Business Projects/    # Ventures, ideas, plans, research
├── Education/            # Certifications, Courses, FDU MBA, Learning_Resources
├── FAMILY TRUST/         # 01_Administration, 02_Finance
├── Finance/
│   ├── Banking/
│   ├── Budget/
│   ├── Credit_Cards/
│   ├── Investments/
│   ├── Loans/
│   ├── Receipts/
│   └── Tax_Returns/
├── Job/                  # Resumes, cover letters
├── Legal/                # Contracts, real estate, insurance, marriage, tickets
├── Personal/
│   ├── Family/
│   ├── Health/
│   ├── Housing/
│   ├── Identity_Documents/
│   ├── Immigration/
│   ├── Insurance/
│   ├── Legal/
│   ├── Travel/
│   ├── Tu Vi/
│   └── Vehicles/
└── Projects/
```

## Mapping Rules

### Legal/
- Notarized mortgage docs (Copie authentique_*)
- Brokerage contracts, promesse d'achat, PAD
- Bail/lease agreements (BAIL, entente de resiliation)
- DRCOP, property listings, inspection reports
- Condo/co-ownership docs
- Gift Fund letters
- Signed employment contracts (if legal in nature)

### Finance/Tax_Returns/
- T4, RELEVE1, RELEVE_PAIE
- Déclaration d'impôts
- État des renseignements (Revenu Québec)
- Notice of assessment
- Tax-related folders (3R, SS état, 2025 tax)

### Finance/Banking/
- Account statements, onlineStatement
- Desjardins statements and zips
- TD, CIBC, RBC docs
- Bell/Videotron bills
- Void cheques, direct deposit forms
- Net worth spreadsheets

### Finance/Investments/
- IBKR statements and zips
- Investment account statements
- Stock research PDFs

### Finance/Receipts/
- Invoices
- Order confirmations
- Shipping receipts

### Business OptCo/RIVIERES/
- Ongles Rivières employment docs (Offre d'emploi, Lettre de confirmation)
- Convention Emploi, Thi Kieu Le Le files
- LE THIEN LAN and other employee PDFs
- Payroll timesheets for Rivières
- Rivières financial statements (SF)

### Business OptCo/SS/
- Sans Souci sales overviews
- Payroll timesheets for Sans Souci

### Business OptCo/MAILY/
- Ongles Maily website saves

### Business OptCo/ (root)
- Cross-business CSVs (customers, attendance)
- BC License.pdf
- Inventory files (fridge_inventory_log, inventory_order)

### Business Projects/
- Salon360/SalonX docs
- Website saves (BLANC NAILS LOUNGE, client_journey)
- Competitor research (abc salonsystem screenshots)

### Personal/
- Pink Card, insurance certificates
- GitHub recovery codes
- Misc personal PDFs

### Personal/Travel/
- Air Canada bookings, flight confirmations

## Process

1. List top-level items in the source directory (Downloads, Desktop, etc.)
2. Present the proposed mapping to the user as a table grouped by destination
3. Let the user confirm or adjust before executing moves
4. Execute moves via Python `shutil.move()` — **always use execute_code, never raw terminal with mv** because filenames contain special characters (&, accented chars, Unicode) that break bash
5. After moves, show final state of source directory

## Pitfalls

- **NEVER use terminal `mv` for bulk file moves.** Filenames with `&`, `'`, accented chars (é, è, ê), and Unicode cause shell escaping failures. Use Python `shutil.move()` via execute_code instead.
- `=?utf-8?B?...` prefixed filenames are base64-encoded — these came from webmail downloads. Move them by exact filename match; they're valid files.
- The `theduylifeos` subfolders already have content — use `shutil.move()` which handles both files and directories, merging into existing folders.
- Pre-existing subfolders in Downloads (Archive, Bo Me, Charlesbourg, Design, Development, Maily, SS, Viet Dung Doan 2025) are the user's intentional staging areas — leave them in place unless the user explicitly says to move them.
- Screenshots and DMGs are temporary junk — create `_Screenshots/` and `_DMGs/` folders inside Downloads rather than polluting theduylifeos.
