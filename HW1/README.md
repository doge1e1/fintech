# 📊 Homework 1: Computing IRR

## 📌 Overview
In this homework, you are required to implement a function to compute the **Internal Rate of Return (IRR)** given a cash flow vector and related parameters.

---

## 🧮 Function Specification

```python
irr = irrFind(cashFlowVec, cashFlowPeriod, compoundPeriod)
Parameters
irr: Internal Rate of Return (output)
cashFlowVec: A list (vector) of cash flows
cashFlowPeriod: Integer representing the cash flow interval (in months)
compoundPeriod: Integer representing the compounding interval (in months)

⚠️ Note: compoundPeriod must be a factor of cashFlowPeriod

Example
cashFlowPeriod = 12
compoundPeriod ∈ {1, 2, 3, 4, 6, 12}
🚀 Usage Examples
irrFind(cashFlowVec, 12, 12)  # yearly payment, yearly compounding
irrFind(cashFlowVec, 12, 3)   # yearly payment, quarterly compounding
irrFind(cashFlowVec, 12, 1)   # yearly payment, monthly compounding
irrFind(cashFlowVec, 3, 1)    # quarterly payment, monthly compounding
🔢 Numerical Examples
irrFind([-1234, 362, 548, 481], 12, 12) -> 0.059616
irrFind([-1234, 362, 548, 481], 12, 1)  -> 0.058047
📥 Input / Output Specification
Input
Each line represents one test case
Maximum 1000 lines
Each line contains:
n cash flow values (n < 20)
followed by:
cashFlowPeriod
compoundPeriod
Values are separated by spaces
Output
Each line should output one IRR value
Format:
Percentage
Rounded to 4 decimal places
▶️ Execution
Main Program
File: goMain.py
Run Command
python goMain.py < inputFile > outputFile
📁 Example Dataset
Input: input0018open.txt
Output: output0018open.txt
⚠️ Important Notes
This assignment is part of Intro to Fintech

IRR range:

-10% ~ 10%
Use similar settings when solving
⏰ Deadline

http://mirlab.org/jang/courses/fintech/homework.asp

🏆 Scoring
Based on correctness over 2000 test cases
Score = ratio of correct answers
⏱️ Time Constraint
Total runtime limit: 2 seconds
❓ FAQ
Do I need to upload goMain.py?

No.
Only upload irrFind.py (no compression required).

How does goMain.py work?
Reads input from STDIN
Writes output to STDOUT
Why is my IRR marked incorrect even when NPV/NFV = 0?
Some cases have multiple valid IRRs
As long as your result is valid, it should be accepted
Any hints for solving IRR?

You can use root-finding methods:

fsolve() → finds one root
roots() → finds all roots

💡 Tip: Use 0 as the initial guess since IRR is usually small

📚 References
Root Finding in Python
fsolve
Course materials (YouTube)
Compounding & IRR theory
