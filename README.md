# 2B — Cold-Pressed Oil Business

**Brand promise:** "Know where your oil comes from."  
**Current stage:** Stage 1 — Research & Validation

---

## How to use this folder

### Every session — start here
Open `00_STATUS.md` first. It tells you:
- What stage you're in
- What's been decided
- The next 3 actions

Do not open anything else until you've read STATUS.

---

## File map

### The 3 files you use regularly

| File | Purpose |
|------|---------|
| `00_STATUS.md` | Current stage, confirmed decisions, next actions — open every session |
| `01_Business/Open_Decisions.md` | Every unanswered question tracked by ID — update when decisions are made |
| `02_Research/Competitor_Research.md` | All-India competitor price table — the active work right now |

### The rest — open only when needed

| File | Open when... |
|------|-------------|
| `01_Business/Business_Plan.md` | You want the full brand, model, and stage picture |
| `03_Product/Groundnut_Oil_v1.md` | Making product, variety, or packaging decisions |
| `03_Product/Batch_Log.md` | You have a real production batch to record |
| `04_Financials/Unit_Economics.md` | You have supplier quotes to plug into the cost model |
| `05_Website_Tech/Tech_Overview.md` | You're ready to start building the website |
| `05_Website_Tech/BRD.md` | Writing website requirements (after product decisions are done) |

---

## Folder structure

```
Cold-Pressed Oil Business\
├── README.md                         ← you are here
├── 00_STATUS.md                      ← open every session
├── 01_Business\
│   ├── Business_Plan.md              ← brand, model, stage gates
│   └── Open_Decisions.md             ← all unanswered questions
├── 02_Research\
│   ├── Competitor_Research.md        ← active research work
│   └── Market_Research_Master.md     ← research questions and method
├── 03_Product\
│   ├── Groundnut_Oil_v1.md           ← product spec, home test, packaging
│   └── Batch_Log.md                  ← production batch records
├── 04_Financials\
│   └── Unit_Economics.md             ← cost, margin, break-even model
└── 05_Website_Tech\
    ├── Tech_Overview.md              ← stack, QR design, existing assets
    └── BRD.md                        ← website requirements (not started)
```

---

## Evidence rules — always apply

| Label | Meaning |
|-------|---------|
| **Confirmed decision** | Decided by the user — lives in `00_STATUS.md` |
| **Observed evidence** | Found in a dated, named source — always cite URL and date |
| **Calculation** | Derived from inputs — show the formula |
| **Assumption** | Not yet proven — label it, do not present as fact |
| **Unknown** | Still needed — write `—`, never guess |

---

## Stage model

| Stage | Name | Where we are |
|-------|------|-------------|
| **1** | **Research** | ← right now |
| 2 | Pilot Test | After research is done |
| 3 | Launch | After pilot proves demand |
| 4 | Scale | After launch is stable |

---

## Key contacts and leads

| Name | Role | Status |
|------|------|--------|
| Sneha Ganuga Oils and Foods | Pressing partner for home test | Lead only — not contacted yet |

---

## Important external links

| Resource | URL |
|----------|-----|
| FSSAI registration | [foscos.fssai.gov.in](https://foscos.fssai.gov.in) |
| React source repo | `cold-oil-react-assets` on GitHub |
| This repo | [github.com/Chaitanyakumargujjala/cold-oil-doc-as-code](https://github.com/Chaitanyakumargujjala/cold-oil-doc-as-code) |

---

## Setting up Kiro and the 2B agent

This repo includes a custom Kiro agent for the 2B oil business at `.kiro/agents/2b-oil-business.json`. The agent knows the full project context — brand decisions, research rules, evidence discipline, and work priority — so you don't have to repeat yourself each session.

### Step 1 — Install Kiro CLI

Download and install Kiro from the official site:

```
https://kiro.dev
```

Verify installation:

```bash
kiro --version
```

### Step 2 — Clone this repo

```bash
git clone https://github.com/Chaitanyakumargujjala/cold-oil-doc-as-code.git
cd cold-oil-doc-as-code
```

### Step 3 — Start a chat session with the 2B agent

Run Kiro chat from inside the cloned folder:

```bash
kiro chat --agent 2b-oil-business
```

Kiro will pick up the agent from `.kiro/agents/2b-oil-business.json` automatically because it's a local agent in the workspace.

You'll see this welcome message:

> 2B Oil Business agent ready. Current priority: all-India groundnut-oil competitor and price research. Project files are at D:\Cold-Pressed Oil Business\. What would you like to work on?

### Step 4 — Start every session with STATUS

Once in chat, the first thing to do is read the status file:

```
read 00_STATUS.md
```

Or just tell the agent what you want to work on — it will read the relevant files before responding.

### Switching to the agent mid-session

If you're already in a Kiro chat session, switch to the 2B agent with:

```
/agent 2b-oil-business
```

Or use the keyboard shortcut: `Ctrl+Shift+2`

### Keeping the repo updated

After any session where decisions were made or research was added:

```bash
git add .
git commit -m "brief description of what changed"
git push
```
