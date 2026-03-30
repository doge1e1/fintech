# 📈 HW02: Trading Strategies Using Technical Indicators

## 🎯 Overview
In this assignment, you are required to design a **stock trading strategy** using **technical indicators (TIs)** covered in class.

Your strategy will be evaluated on both a **public dataset** and a **private dataset**, and you will compete with other students on Gradescope.

Final score:

(public_score + private_score) / 2


---

## 🎥 Instructional Video
https://www.youtube.com/watch?v=i1DisY9ARzA

---

## 📁 File Structure


.
├── bestParamByExhaustiveSearch.py # Parameter optimization
├── myStrategy.py # Your trading strategy (submission file)
├── rrEstimate.py # Backtesting tool
├── public.csv # Public dataset
├── readme.txt


---

## 🧠 Design Workflow

1. **Select Technical Indicators (TIs)**
   - Use indicators covered in class (e.g., MA, MACD, RSI)
   - Or design your own indicator

2. **Define Trading Strategy**
   - Buy / Sell rules based on indicators
   - Include tunable parameters

3. **Parameter Optimization**
   - Use historical data to find best parameters

4. **Performance Evaluation**
   - Test optimized strategy on longer datasets

---

## ⚙️ Example Workflow

### Step 1: Find Best Parameters
```bash
python bestParamByExhaustiveSearch.py public.csv

Example output:

Best settings: fast_period=8, slow_period=24, signal_period=9 ==> returnRate=0.007356
Step 2: Apply Strategy

Put best parameters into myStrategy.py, then run:

python rrEstimate.py public.csv

Example output:

rr=0.735616%
⚠️ Important Constraints
Only use historical data up to current day
Only technical indicators are allowed
❌ Machine Learning / Neural Networks / DP not allowed in myStrategy.py
Strategy must be deterministic
❌ No randomness
Runtime constraint:
Each myStrategy() call ≤ 0.01 sec
Timeout → default action = 0 (hold)
📊 Scoring
Based on Return Rate
Dataset:
Public (~2400 days)
Private (~2400 days)
Score Display
Before deadline: Public score only
After deadline: Final score
Final Score = (public + private) / 2
🧪 Environment

Available packages on Gradescope:

pandas==2.2.2
numpy==2.1.1
scipy==1.14.1
statsmodels==0.14.2
🚫 Restrictions
❌ No machine learning in myStrategy.py
❌ No randomness
❌ No external libraries beyond allowed packages
❓ FAQ
Q1: How is the score calculated?

Based on Return Rate, using a predefined scoring table.

Q2: What is "Public Time Used"?
Total backtesting time (not per function)

Time limits:

Each myStrategy() ≤ 0.01 sec
Timeout → action = 0
Q3: Can I use ML?
In myStrategy.py: ❌ Not allowed
For parameter tuning: ✅ Allowed
Q4: Why did I get 60 points?

Possible reasons:

Return rate too low
Wrong filename (myStrategy.py)
Upload failed
Syntax error
Import error
📌 Submission
Upload only:
myStrategy.py
💡 Tips
Start with simple indicators (MA crossover, RSI)
Focus on 穩定報酬 > 極端高報酬
Optimize parameters carefully
Avoid overfitting to public dataset
📚 Keywords
Technical Indicators
Trading Strategy
Backtesting
Return Rate Optimization
