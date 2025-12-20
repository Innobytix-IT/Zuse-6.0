Hier ist die Übersetzung der Dokumentation ins Englische. Ich habe dabei auch die Code-Beispiele in den Syntax-Abschnitten auf die **englische Zuse-Syntax** angepasst (z.B. `IF` statt `WENN`), damit internationale Nutzer die Sprache sofort verstehen.

Du kannst das als `README.md` (oder `README_EN.md`, falls du beide behalten willst) speichern.

***

```markdown
# ZUSE 🖥️
> **"Simple because 'Simple' is simple."**

![Version](https://img.shields.io/badge/Version-6.x-blue) ![Language](https://img.shields.io/badge/Made_with-Python-yellow) ![Status](https://img.shields.io/badge/Status-Stable-green)

**Zuse** is an object-oriented, interpreted programming language designed to break the barrier between "Learning Languages" (like Scratch) and "Pro Languages" (like Python/C++).

It enables programming in your native language (DE, EN, ES, PT, FR, IT) and offers a seamless transition from simple graphics programming to controlling complex hardware.

---

## 🚀 Features

*   **🌍 Multilingual:** The interpreter understands 6 languages natively (German, English, Spanish, Portuguese, French, Italian).
*   **🛡️ Dual Mode:**
    *   **Learning Mode:** Sandbox environment for kids/beginners (safe commands only).
    *   **Pro Mode ("God Mode"):** Full access to the Python Runtime (including hardware control).
*   **🧠 Environment Aware:** Zuse automatically detects whether it is running inside the IDE or as a standalone application and adapts window management dynamically.
*   **🎨 Zuse Studio:** A custom IDE with syntax highlighting, live translation, and GUI-Block-Mode.

---

## 🛠️ System Architecture

Zuse is based on a **3-Layer Architecture**:

### 1. The Core (Interpreter)
The engine (`interpreter.py`) is based on Python. It features a **Smart Import Mechanism** that prevents language libraries from being loaded twice and recognizes constructors across languages (`ERSTELLE`, `NEW`, `CREAR`, etc.).

### 2. The IDE (Zuse Studio)
The Studio (`zuse_studio.py`) is thread-safe and includes **Pre-Flight-Check** logic. It warns the user before execution if graphical commands are used but the necessary GUI Mode is not activated.

### 3. The Standard Library (Smart Layer)
The `.zuse` files in the `bibliothek/` folder are intelligent wrappers.
*   **Example `CLASS Window`:** Encapsulates `tkinter`. Automatically decides whether to create a `tk.Tk()` (Standalone) or a `tk.Toplevel()` (Studio) and forces keyboard focus in Studio (`grab_set`).
*   **Example `CLASS Painter`:** Encapsulates `turtle`. Includes an "Anti-Zombie-Fix" (`clearscreen` + `_RUNNING=True`) to prevent crashes during restarts.

---

## 📚 Syntax Examples (English)

### Hello World & Logic
```text
text = "Hello Zuse"
number = 42

IF number > 10 THEN
    PRINT text
ELSE
    PRINT "Number is small"
END IF
```

### Loops
```text
LOOP FOR i IN [1, 2, 3] DO
    PRINT "Iteration: " + str(i)
END LOOP
```

### Object Orientation
```text
CLASS Robot:
    DEFINE NEW(name):
        SELF.name = name
    END FUNCTION

    DEFINE hello():
        PRINT "I am " + SELF.name
    END FUNCTION
END CLASS

r1 = Robot("ZuseBot")
r1.hello()
```

### Graphics (The Painter)
```text
IMPORT english
pablo = Painter()

pablo.color("blue")
pablo.width(5)

LOOP FOR i IN [1, 2, 3, 4] DO
    pablo.move(100)
    pablo.turn_right(90)
END LOOP
```

---

## 🕹️ Usage

### Start the IDE
```bash
python zuse_studio.py
```

### Run a Program (Standalone)
```bash
python main.py my_script.zuse english
```

---

## 🔌 Hardware & Deployment

Thanks to **Pro Mode**, Zuse can access hardware directly.

**Example: Controlling Arduino**
```text
IMPORT pyfirmata
board = pyfirmata.Arduino("COM3")
led = board.get_pin("d:13:o")
led.write(1)
```

**Current Projects:**
*   **Infotainment PeugeotDash / Car-PC:** An Arduino shutdown controller is being built for this, with logic written in Zuse.

---

## 🗺️ Roadmap (Zuse: The Universal Vision)

*   [x] **v1.0 (v6.9):** Stable Interpreter, IDE, Libraries (DE/EN/ES/PT/FR/IT).
*   [ ] **v2.0 (Zuse Universal):** Decoupling from Python Core via an **Intermediate Representation (IR)**. Development of a transpiler to **JavaScript** (among others like **C#** and **Java**) to execute Zuse programs natively in the browser (e.g., as PWA).

---

**Architect:** Manuel Person
**Co-Coding:** Gemini
**License:** Open Source MIT
```