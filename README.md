# 🐇🏹 Hunter–Rabbit Simulation (IMO 2017, Problem 3)

This repository contains numerical simulations of the pursuit–evasion game from **IMO 2017, Problem 3**.  
The goal is to understand how the rabbit can guarantee a large escape distance after 10^9 steps and how discretization (rounding to unit steps) affects the pursuit dynamics.
We compare two frameworks:

1. **Modified Assumptions Model** — cycles may have real-valued length $L = aD$.  
2. **Original Olympiad Rules Model** — every move must be **exactly 1 unit**, so cycles use $L = \lceil aD \rceil$.

All geometric updates follow Evan Chen’s exposition:  
https://web.evanchen.cc/exams/IMO-2017-notes.pdf

---

## ⭐ Mathematical Overview

### Distance recurrence

If both the rabbit and the hunter advance by $L$ units in the same cycle, the new separation satisfies

$$
D_{\text{new}} = \sqrt{(\sqrt{L^2-1}-L+D)^2+1}.
$$

Difference between models:

- **Modified model:**

$$
L = aD
$$

- **Original IMO rules:**

$$
L = \lceil aD \rceil.
$$

---

## 📁 File Structure

    hunter-rabbit-simulation-IMO2017-problem-3/
    │
    ├── hunter_rabbit_modified_assumptions_float.py
    ├── hunter_rabbit_modified_assumptions_hp.py
    ├── hunter_rabbit_original_rules_hp.py
    │
    ├── compare_errors_modified_assumptions.py
    ├── compare_D_and_angle_original_and_modified.py
    │
    ├── requirements.txt
    ├── README.md
    ├── .gitignore
    └── setup.sh

---

## 🚀 Installation & Running

### 1. Clone the repository

    git clone https://github.com/jakolsz11/hunter-rabbit-simulation-IMO2017-problem-3.git
    cd hunter-rabbit-simulation-IMO2017-problem-3

### 2. Set up the virtual environment (macOS / Linux)

    ./setup.sh

This script automatically:
- creates a virtual environment `.venv`,
- installs all required dependencies from `requirements.txt`.

### 3. Activate the virtual environment

    source .venv/bin/activate

### 4. Run simulations

Examples:

    python hunter_rabbit_original_rules_hp.py
    python hunter_rabbit_modified_assumptions_hp.py
    python compare_errors_modified_assumptions.py
    python compare_D_and_angle_original_and_modified.py

### 5. Adjust parameters

You can experiment with different values of the parameter `a` by editing it directly inside each script, for example:

    a = 1.01

### 6. Deactivate the environment after finishing work

    deactivate 

### Windows users

The `setup.sh` script is intended for macOS / Linux.

On Windows, please set up the environment manually:

```bat
python -m venv .venv
.venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

---

## ⚙️ Why do we use $\lceil aD \rceil$?

IMO rules enforce:

- each move has length exactly $1$,  
- a cycle should use the maximum number of full unit steps,  
- so the ideal continuous length $aD$ becomes

$$
L = \lceil aD \rceil.
$$

This strictly satisfies the Olympiad constraint while preserving the geometric strategy.

---

## 🧠 Future Directions

- analysis of how the parameter $a$ affects the **total number of unit steps** required for the rabbit to reach a safe distance (e.g. $D \ge 100$)  
- studying the growth of the distance $D_n$ measured in **individual unit moves**, not just in aggregated cycles  
- optimisation of escape strategies under the constraint “each move has length 1”  
- reinforcement learning / AI for rabbit and hunter  
