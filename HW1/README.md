
##Homework 1: Computing IRR
Goal
In this homework, you need to write a function to compute IRR (internal rate of return) given a vector of cash flow and some related parameters.

Function prototype
irr=irrFind(cashFlowVec, cashFlowPeriod, compoundPeriod)
irr: Internal rate of return
cashFlowVec: vector of cash flow
cashFlowPeriod: An integer of period (in month) for cash flow
compoundPeriod: An integer of period (in month) for compounding, which should be a factor of cashFlowPeriod. (For instance, if cashFlowPeriod=12, compoundPeriod could be 1, 2, 3, 4, 6, 12.)
Usage examples
irrFind(cashFlowVec, 12, 12): Yearly payment/collection, yearly compounding
irrFind(cashFlowVec, 12, 3): Yearly payment/collection, quarterly compounding
irrFind(cashFlowVec, 12, 1): Yearly payment/collection, monthly compounding
irrFind(cashFlowVec, 3, 1): quarterly payment/collection, monthly compounding
Numerical examples
irrFind([-1234,362,548,481], 12, 12) returns 0.059616
irrFind([-1234,362,548,481], 12, 1) returns 0.058047
Test Specs
I/O format
Input file specs
Each line is a test case, with no more than 1,000 lines.
Each line has n+2 integers (n<20) separated by a space, with the first n integers as cash flow vector, and the last two elements as periods for cash flow and compounding, respectively.
Main program
goMain.py (Press right button on the link to download it.)
Usage: python goMain.py < inputFile > outputFile
Output specs
Each line contains a single number of IRR in percentage, with four decimal places
Example files
Dataset 1 of 18 cases:
Input file: input0018open.txt
Output file: output0018open.txt
Important facts
Judge system for "Intro. to Fintech"
The interest rate is always between -10% and 10%.
You should try to use the same settings.
Deadline: [http://mirlab.org/jang/courses/fintech/homework.asp]
Scoring: Ratio of correctly computed cases in another dataset of 2000 cases.
Total computing time constraint: 2 sec
FAQ
Do I need to upload the main program "goMain.py"?

Ans: No, you only need to upload "irrFind.py" directly, with no compression.

How to use "goMain.py"?

Ans: The main program takes STDIN as input and STDOUT as output.

How come the IRR I derived leads to a zero NPV/NFV, but the judge system still thinks the IRR is not correctly?

Ans: There might be several legitimate IRRs (within the right range) for a given test case. As long as your put one of them into the output file, then the case will be considered solved.

Do you have some hints about solving the NPV/NFV equations?

Ans: You can use either fsolve() or roots().

fsolve() can only find a root at a time. (Since IRR is usually a small number, you can set the initial guess as 0.)
roots() can find all the roots simultaneously.
References
Root Finding
Root Finding in Python
fsolve
Course material on youtube
Compounding
IRR