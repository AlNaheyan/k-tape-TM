# Turing Machine Project  
**Author:** Al Naheyan  
**NetID:** 24417056  
**Course:** Theory of Computer Science  

---

## 1. Overview

This project implements a fully functional **multi-tape Turing Machine simulator**.  
The simulator:

- Reads machine descriptions in the CSV format specified in the project handout  
- Supports *k* tapes  
- Supports blank (`_`) symbols  
- Supports wildcards (`*`) for transitions  
- Halts on **Accept**, **Reject**, or **Error**  
- Prints full step-by-step execution traces  

All instructor machines were executed and validated, and two custom machines were designed and tested as required.

---

## 2. Instructor Machines

### **TM1 — Single-Tape Transformation**
- Performs simple symbol rewriting and scanning behavior.  
- All instructor tests matched the expected output.

### **TM1d — Decider for Patterned Binary Strings**
- Determines whether input matches a mirrored pattern separated by `#`.  
- All strings in `TM1-accept.txt` were **Accepted**.  
- All strings in `TM1-reject.txt` correctly produced **Error**.  
- Confirms proper halting and correct acceptance conditions.

### **TM2 — Two-Tape Machine**
- Exercises multi-tape movement and rewriting logic.  
- All test outputs match instructor expectations.

### **TM3 — Three-Tape Machine**
- Demonstrates copying, marking, and recombination across three tapes.  
- All tests halted in **Accept** with correct final tape contents.


---

## 3. Custom Machine #1 — EvenOnes-24417056

### **Description**
A decider for the language:

\[
L = \{ w \in \{0,1\}^* \mid \text{the number of ‘1’s in } w \text{ is even} \}
\]

Uses one tape and two parity states:

- `q0` = even number of 1s  
- `q1` = odd number of 1s  

### **Behavior**
- Read `0` → stay in same state  
- Read `1` → toggle between `q0` and `q1`  
- Read `_` → Accept in `q0`, Reject in `q1`  

### **Tests Performed**
Tested on:  
`0, 1, 10, 11, 101, 1010, 1111, 10101, 000`

Correct results:  
- **Accepted:** `0`, `10`, `11`, `1010`, `1111`, `000`  
- **Rejected:** `1`, `101`, `10101`

Machine halts on all inputs and behaves as expected.

---

## 4. Custom Machine #2 — CopyToTape2-24417056

### **Description**
A 2-tape machine that copies the entire contents of **Tape 1** onto **Tape 2** and then halts in Accept.

### **Behavior**
- Read `0` → write `0` to Tape 2, move both heads right  
- Read `1` → write `1` to Tape 2, move both heads right  
- Read `_` → move to Accept state  

Tape 1 is unchanged; Tape 2 becomes an exact duplicate.

### **Tests Performed**
Inputs tested:  
`101`, `1111`, `0`, `101010`

Results:  
- Tape 2 matched Tape 1 exactly  
- Machine halted in Accept every time

---

## 5. Running the Simulator

Run the simulator using:

```bash
python3 tm_24417056.py <machinefile> <tapefile>