# Minesweeper AI

A **logic-based AI** that plays Minesweeper using **symbolic reasoning and set-based inference**. This project demonstrates **constraint satisfaction, reasoning over uncertain information, and integration with a graphical interface**.

---
## 🧠 Features

- **AI Reasoning Engine**:  
  - Tracks **safe cells** and **mines** as sets.  
  - Forms **logical sentences** representing a group of unknown cells and the number of mines among them.  
  - Performs **subset-based inference**:
    - If all cells in a sentence are mines, they are added to the mine set.
    - If the number of mines is zero, all cells are safe.
    - New sentences are inferred by comparing subsets of cells across existing sentences.
  - Continuously updates its knowledge as moves are made.

- **Interactive GUI**:  
  - Built using `pygame`.  
  - Clickable grid cells with flagging functionality.  
  - AI can suggest a safe move or make a random move when uncertain.  
  - Dynamic board resizing.

- **AI Log Panel**:  
  - Shows step-by-step reasoning of AI decisions.  
  - Logs set-based inferences: which groups of cells are analyzed, and which new safe or mine cells are inferred.

- **Customizable Game Settings**:  
  - Adjustable board size (`WIDTH`, `HEIGHT`) and number of mines (`MINES`).  
  - Responsive interface for different screen sizes.

---

## ⚙️ How the AI Thinks
1. The AI maintains **3 sets**:
- `safes` - cells known to be safes
- `mines` - cells known to be mines
- `moves_made` - cells already clicked.

2. Each revealed cell creates a **sentence**:
A set of neighboring cells and the count of mines among them:
**For example**: ```{A, B, C, D, E, F, G, H} = 1```



3. **Inference using sets**:
- If `count == 0`, all cells in the set r set to be safe.
- If `count == length of set`, all cells in the set are marked as mines.
- Subset Logic:
    - If one set is  a subset of another, the difference can generate a **new sentence** with updated mine count. 

4. AI repeats this process iteratively **until no new inferences** can be made for which it makes a random move to a cell which it thinks will be safe.



