# Release Notes: OnyxScript v1.0.0-alpha ðŸŽ‰

Welcome to the very first public release of **OnyxScript**! This version introduces the foundational core of the language, designed to make application development highly intuitive, readable, and efficient.

## ðŸš€ Key Features

*   **English-Like Syntax:** Write clean, expressive code that reads naturally, drastically lowering the learning curve for new developers.
*   **Rapid Development:** Build functional application logic in as few as 10 lines of code.
*   **Modular Architecture:** Built-in support for extending functionality via modules.
*   **Lightweight Execution:** Highly optimized compiler/interpreter core ensuring minimal system footprint.

---

## ðŸ“¦ What's Included in This Build

This release provides the absolute minimum viable ecosystem required to execute your first OnyxScript code:
1.  **OnyxScript Core Engine:** The main executable/binary responsible for parsing and running your code.
2.  **Sample Configurations:** Core framework templates to kickstart your project structure.
3.  **Command Execution Scripts:** Pre-configured paths for rapid command line testing.

---

## ðŸ› ï¸ Installation & Setup Guide

Getting started with OnyxScript takes less than a minute:

1.  **Download:** Download the compiled archive (`OnyxScript-v1.0.0.zip` or `.tar.gz`) from the Assets section below.
2.  **Extract:** Extract the files to a permanent directory on your local machine (e.g., `C:\OnyxScript` or `~/onyxscript`).
3.  **Add to Environment Path (Optional but Recommended):**
    *   Add the installation directory to your system's `PATH` variables to run the compiler from any terminal environment.
4.  **Verify Installation:** Run the following command in your terminal or command prompt:
    ```bash
    onyx --version
    ```

---

## ðŸ’» Writing Your First "10-Line App"

Create a new file named `app.onyx` and paste the following baseline template:

```onyx
// OnyxScript Basic Application Template
import core.modules.ui

initialize application "My First App"
set window width 800
set window height 600

render visible element:
    display text "Hello, World!" at position (center)
    create interactable button "Click Me" triggers click_action

define action click_action:
    notify user "Button was successfully clicked!"
```

To run your code, simply execute:
```bash
onyx run app.onyx
```

---

## ðŸ›¡ï¸ Security & Transparency Disclaimer

To ensure absolute trust and safety within our developer community:
*   **Source Code Inspection:** The complete source framework will be pushed directly to the `main` branch shortly. We encourage everyone to audit, fork, and review the code.
*   **VirusTotal Verified:** This compiled release has been pre-verified. [View the Clean VirusTotal Scan Report](https://www.virustotal.com/) (Replace this placeholder text with your actual VirusTotal scan link to eliminate any potential antivirus false positives).

---

## ðŸ› Known Issues & What's Next

As an initial alpha launch, you may encounter edge-case bugs:
*   *UI layout scaling on high-DPI displays may require manual padding adjustments.*
*   *Error exceptions inside deeply nested modules can occasionally report vague line numbers.*

**Upcoming in v1.1.0:** Enhanced error debugging outputs, cross-platform mobile compilation capabilities, and an official VS Code extension syntax highlighter!