# RSA Laboratory

## 👥 Team Members
* **Jair Mendoza (269615):** Environment and communication logic.
* **Kiroloes Ghebrial (294502):** Intercept and decryption logic.

---

## 🚀 Usage

### 🖥️ Terminal
Each script must be run in a **separate terminal window**. Launch them in the following order:

1. `python channel.py` - Starts the relay that forwards messages
2. `python bob.py` - Starts Bob (receiver)
3. `python eve.py` - Starts Eve (eavesdropper)
4. `python alice.py` - Starts Alice (sender)

> **Note:** Bob, Eve, and Channel keep running. You can run Alice many times without restarting the others.

#### 📨 Sending Messages with Alice
When `alice.py` runs, you can type messages in its terminal:

| Command | What it does |
|---------|---------------|
| `Hello Bob` | Sends a short message |
| `large:Your long text here` | Sends a long message (splits into blocks) |
| `quit` | Closes Alice's connection |

