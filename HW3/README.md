# 📊 HW04: Optimum Strategy for Stock Trading with Known Future Prices

## 🎯 Overview
This assignment focuses on designing **optimal trading strategies** when stock prices are fully or partially known.

You will implement strategies to maximize return under different constraints, including:
- Full future price knowledge (offline mode)
- Limited future knowledge (online mode)

---

## 🧠 Problem Description

We consider:
- Multiple stocks
- Known transaction costs
- Constraints on trading behavior

Goal:
> Maximize total return rate through optimal buy/sell decisions

---

## 📥 Input Description

### Price Matrix
- `priceMat`: Matrix of size **(days × stocks)**
- Each entry represents stock price at a given day

### Transaction Costs
- `rate1`: Buy fee (~0.1425%)
- `rate2`: Sell fee (~0.4425%)

---

## 📤 Output Format

```python
actionMat = myAction01(priceMat, rate1, rate2)

Each action is:

[day, fromStock, toStock, amount]
Definition
day: trading day (starting from 0)
fromStock:
-1 → cash
otherwise → stock index
toStock:
same rule as above
amount: cash used (must be positive)
📌 Example Actions
[5, -1, 7, 100]  # buy stock 7 with cash
[3, 8, -1, 50]   # sell stock 8

⚠️ Stock-to-stock exchange is NOT allowed
You must sell first, then buy in another transaction

⚠️ Trading Constraints
Only one transaction per day
Cooldown period: 2 days
After trading, must wait 2 days before next trade
Trading allowed on:
First day ✅
Last day ✅ (final value converted to cash)
No direct stock-to-stock swap
🧩 Tasks
🔹 Task 1: myAction01()
Full future prices available
Goal: maximize return
Methods:
Greedy
Dynamic Programming (recommended)
🔹 Task 2: myAction02()
Limited number of transactions (K given by TA)
Optimize under transaction constraint
🔹 Task 3: myAction03()
Online decision making
Only know:
Past prices
Next-day prices
action = myAction03(priceMatHistory, priceMatFuture, position, actionHistory, rate1, rate2)
📊 Online Mode Inputs
priceMatHistory: past price data
priceMatFuture: next-day price
position: current holdings
actionHistory: past actions
Position Example
[2, 3, 1, 6, 200]
Stocks: 2, 3, 1, 6 units
Cash: 200
🧪 Testing

Run:

python rrEstimateOpen.py priceMat0992.txt 0.001425 0.004425

Example result:

18931.082700%
📁 Files
.
├── myAction.py             # Your implementation (submit this)
├── rrEstimateOpen.py       # Evaluation script
├── priceMatXXXX.txt        # Dataset
📌 Submission
Upload only:
myAction.py
⏱️ Constraints
Total runtime ≤ 5 minutes
Invalid action format → score = 0
🏆 Scoring

Final score is based on rankings of:

myAction01() → return rate ranking
myAction02() → average ranking (different K)
myAction03() → return rate ranking
💡 Strategy Ideas
Greedy (baseline)
Dynamic Programming (best for offline)
Momentum-based strategies (online)
Trend following / reversal detection
📚 References
Dynamic Programming for Trading
Multi-asset portfolio optimization
