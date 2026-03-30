import numpy as np

# A simple greedy approach
def myActionSimple(priceMat, transFeeRate):
    # Explanation of my approach:
	# 1. Technical indicator used: Watch next day price
	# 2. if next day price > today price + transFee ==> buy
    #       * buy the best stock
	#    if next day price < today price + transFee ==> sell
    #       * sell if you are holding stock
    # 3. You should sell before buy to get cash each day
    # default
    cash = 1000
    hold = 0
    # user definition
    nextDay = 1
    dataLen, stockCount = priceMat.shape  # day size & stock count   
    stockHolding = np.zeros((dataLen,stockCount))  # Mat of stock holdings
    actionMat = []  # An k-by-4 action matrix which holds k transaction records.
    
    for day in range( 0, dataLen-nextDay ) :
        dayPrices = priceMat[day]  # Today price of each stock
        nextDayPrices = priceMat[ day + nextDay ]  # Next day price of each stock
        
        if day > 0:
            stockHolding[day] = stockHolding[day-1]  # The stock holding from the previous action day
        
        buyStock = -1  # which stock should buy. No action when is -1
        buyPrice = 0  # use how much cash to buy
        sellStock = []  # which stock should sell. No action when is null
        sellPrice = []  # get how much cash from sell
        bestPriceDiff = 0  # difference in today price & next day price of "buy" stock
        stockCurrentPrice = 0  # The current price of "buy" stock
        
        # Check next day price to "sell"
        for stock in range(stockCount) :
            todayPrice = dayPrices[stock]  # Today price
            nextDayPrice = nextDayPrices[stock]  # Next day price
            holding = stockHolding[day][stock]  # how much stock you are holding
            
            if holding > 0 :  # "sell" only when you have stock holding
                if nextDayPrice < todayPrice*(1+transFeeRate) :  # next day price < today price, should "sell"
                    sellStock.append(stock)
                    # "Sell"
                    sellPrice.append(holding * todayPrice)
                    cash = holding * todayPrice*(1-transFeeRate) # Sell stock to have cash
                    stockHolding[day][sellStock] = 0
        
        # Check next day price to "buy"
        if cash > 0 :  # "buy" only when you have cash
            for stock in range(stockCount) :
                todayPrice = dayPrices[stock]  # Today price
                nextDayPrice = nextDayPrices[stock]  # Next day price
                
                if nextDayPrice > todayPrice*(1+transFeeRate) :  # next day price > today price, should "buy"
                    diff = nextDayPrice - todayPrice*(1+transFeeRate)
                    if diff > bestPriceDiff :  # this stock is better
                        bestPriceDiff = diff
                        buyStock = stock
                        stockCurrentPrice = todayPrice
            # "Buy" the best stock
            if buyStock >= 0 :
                buyPrice = cash
                stockHolding[day][buyStock] = cash*(1-transFeeRate) / stockCurrentPrice # Buy stock using cash
                cash = 0
                
        # Save your action this day
        if buyStock >= 0 or len(sellStock) > 0 :
            action = []
            if len(sellStock) > 0 :
                for i in range( len(sellStock) ) :
                    action = [day, sellStock[i], -1, sellPrice[i]]
                    actionMat.append( action )
            if buyStock >= 0 :
                action = [day, -1, buyStock, buyPrice]
                actionMat.append( action )
    return actionMat

# A DP-based approach to obtain the optimal return
def myAction01(priceMat, transFeeRate):
    totalDays, stockCount = priceMat.shape
    cash = 1000
    
    # 創建DP表格
    # dp_cash[i]: 第i天持有現金的最大金額
    # dp_stock[i][j]: 第i天持有股票j的最大數量
    dp_cash = [0] * totalDays
    dp_stock = np.zeros((totalDays, stockCount))
    
    # 記錄最佳選擇的來源
    # source[i][j]: 第i天狀態j的最佳來源 (-1表示現金，0~stockCount-1表示股票)
    source = np.full((totalDays, stockCount + 1), -2)  # +1 for cash state
    
    # 初始化第0天
    dp_cash[0] = cash
    for j in range(stockCount):
        dp_stock[0][j] = cash * (1 - transFeeRate) / priceMat[0][j]
    
    # 填充DP表格
    for i in range(1, totalDays):
        # 計算持有現金的情況
        dp_cash[i] = dp_cash[i-1]  # 保持現金
        source[i][stockCount] = -1  # stockCount索引表示現金狀態
        
        # 檢查從各個股票轉換到現金的情況
        for j in range(stockCount):
            cash_amount = dp_stock[i-1][j] * priceMat[i][j] * (1 - transFeeRate)
            if cash_amount > dp_cash[i]:
                dp_cash[i] = cash_amount
                source[i][stockCount] = j
        
        # 計算持有每支股票的情況
        for j in range(stockCount):
            # 1. 保持原有持股
            dp_stock[i][j] = dp_stock[i-1][j]
            source[i][j] = j
            
            # 2. 從現金買入
            stock_from_cash = dp_cash[i-1] * (1 - transFeeRate) / priceMat[i][j]
            if stock_from_cash > dp_stock[i][j]:
                dp_stock[i][j] = stock_from_cash
                source[i][j] = -1
            
            # 3. 從當前現金買入（如果現金是從其他股票賣出得到的）
            stock_from_current_cash = dp_cash[i] * (1 - transFeeRate) / priceMat[i][j]
            if stock_from_current_cash > dp_stock[i][j]:
                dp_stock[i][j] = stock_from_current_cash
                source[i][j] = -1
    
    # 回溯找出最佳交易序列
    actionMat = []
    
    # 找出最後一天的最佳狀態
    current_state = stockCount  # 從現金狀態開始
    max_final_value = dp_cash[totalDays-1]
    
    for j in range(stockCount):
        final_stock_value = dp_stock[totalDays-1][j] * priceMat[totalDays-1][j] * (1 - transFeeRate)
        if final_stock_value > max_final_value:
            max_final_value = final_stock_value
            current_state = j
    
    # 從最後一天往回追溯
    for i in range(totalDays-1, 0, -1):
        prev_state = source[i][current_state]
        
        if prev_state != current_state and prev_state != -2:
            if current_state == stockCount:  # 現金狀態
                if prev_state != -1:  # 從股票轉為現金
                    actionMat.append([i, prev_state, -1, 
                                    dp_stock[i-1][prev_state] * priceMat[i][prev_state]])
            else:  # 股票狀態
                if prev_state == -1:  # 從現金轉為股票
                    actionMat.append([i, -1, current_state, 
                                    dp_cash[i-1] if i > 0 else cash])
                elif prev_state != current_state:  # 從一支股票轉為另一支
                    actionMat.append([i, prev_state, current_state,
                                    dp_stock[i-1][prev_state] * priceMat[i][prev_state]])
        
        current_state = prev_state if prev_state != -2 else current_state
    
    # 處理第一天的交易（如果有）
    if current_state >= 0 and current_state < stockCount:
        actionMat.append([0, -1, current_state, cash])
    
    # 反轉序列以得到正確的時間順序
    actionMat.reverse()
    
    return actionMat

# An approach that allow non-consecutive K days to hold all cash without any stocks
def myAction02(priceMat, transFeeRate, K):
    """
    Trading strategy function that optimizes holding periods using earning rates.
    
    Args:
        priceMat: Price matrix for stocks over time
        transFeeRate: Transaction fee rate
        K: Target number of days to hold cash
        
    Returns:
        actionMat: List of trading actions [day, from_pos, to_pos, amount]
    """
    import numpy as np
    
    totalDays, stockCount = priceMat.shape
    cash = 1000
    actionMat = []
    
    # Initialize holdings arrays
    stockHolding = np.zeros((totalDays, stockCount))
    cashHolding = np.zeros(totalDays)
    cashHolding[0] = cash
    
    # Initialize first day stock holdings
    stockHolding[0] = cash * (1-transFeeRate) / priceMat[0]
    
    def update_holdings(start_day, end_day, earning_rate_periods=None):
        """
        Update holdings between given days, optionally considering earning rate periods
        
        Args:
            start_day: Starting day for update
            end_day: Ending day for update
            earning_rate_periods: List of [day, rate] pairs for forced cash holding
        """
        for i in range(start_day, end_day):
            if earning_rate_periods is not None:
                curr_period = next((p for p in earning_rate_periods if p[0] == i), None)
                next_period = next((p for p in earning_rate_periods if p[0] == i + 1), None)
                
                if curr_period is not None:
                    # Force cash holding, sell all stocks
                    cashHolding[i] = cashHolding[i-1]
                    for j in range(stockCount):
                        stockHolding[i][j] = 0
                        sale_value = stockHolding[i-1][j] * priceMat[i][j] * (1-transFeeRate)
                        cashHolding[i] = max(cashHolding[i], sale_value)
                    continue
                    
                if next_period is not None and curr_period is None:
                    # Reinvest in stocks
                    cashHolding[i] = cashHolding[i-1]
                    stockHolding[i] = cashHolding[i-1] * (1-transFeeRate) / priceMat[i]
                    continue
            
            # Normal holding update
            cashHolding[i] = cashHolding[i-1]
            for j in range(stockCount):
                sale_value = stockHolding[i-1][j] * priceMat[i][j] * (1-transFeeRate)
                cashHolding[i] = max(cashHolding[i], sale_value)
            
            for j in range(stockCount):
                prev_holding = stockHolding[i-1][j]
                buy_from_prev = cashHolding[i-1] * (1-transFeeRate) / priceMat[i][j]
                buy_from_curr = cashHolding[i] * (1-transFeeRate) / priceMat[i][j]
                stockHolding[i][j] = max(prev_holding, buy_from_prev, buy_from_curr)
    
    def count_cash_days():
        """Count consecutive days holding cash position"""
        cash_days = 0
        position = -1
        
        for i in range(totalDays-1, 0, -1):
            if position == -1:
                cash_days += 1
                if cashHolding[i] != cashHolding[i-1]:
                    for j in range(stockCount):
                        if abs(cashHolding[i] - stockHolding[i-1][j] * priceMat[i][j] * (1-transFeeRate)) < 1e-10:
                            position = j
                            break
            else:
                if abs(stockHolding[i][position] - cashHolding[i-1] * (1-transFeeRate) / priceMat[i][position]) < 1e-10:
                    position = -1
                elif abs(stockHolding[i][position] - cashHolding[i] * (1-transFeeRate) / priceMat[i][position]) < 1e-10:
                    for j in range(stockCount):
                        if abs(cashHolding[i] - stockHolding[i-1][j] * priceMat[i][j] * (1-transFeeRate)) < 1e-10:
                            position = j
                            break
        
        return cash_days
    
    # Initial holdings calculation
    update_holdings(1, totalDays)
    
    # Calculate earning rates
    earning_rates = [[i, (cashHolding[i+1] - cashHolding[i])/cashHolding[i]] 
                    for i in range(1, totalDays-1)]
    earning_rates.sort(key=lambda x: x[1])
    
    # Iteratively adjust cash holding periods
    cash_days = count_cash_days()
    list_end_idx = int((K-cash_days)/2)
    
    while cash_days < K and list_end_idx <= len(earning_rates):
        current_periods = earning_rates[:list_end_idx]
        update_holdings(1, totalDays, current_periods)
        cash_days = count_cash_days()
        list_end_idx += int((K-cash_days)/2 + 1)
    
    # Generate final action matrix
    position = -1
    for i in range(totalDays-1, 0, -1):
        if position == -1:
            if cashHolding[i] == cashHolding[i-1]:
                continue
            for j in range(stockCount):
                if abs(cashHolding[i] - stockHolding[i-1][j] * priceMat[i][j] * (1-transFeeRate)) < 1e-10:
                    position = j
                    actionMat.append([i, position, -1, stockHolding[i-1][j] * priceMat[i][j]])
                    break
        else:
            if abs(stockHolding[i][position] - cashHolding[i-1] * (1-transFeeRate) / priceMat[i][position]) < 1e-10:
                action_pos = position
                position = -1
                actionMat.append([i, position, action_pos, cashHolding[i-1]])
            elif abs(stockHolding[i][position] - cashHolding[i] * (1-transFeeRate) / priceMat[i][position]) < 1e-10:
                for j in range(stockCount):
                    if abs(cashHolding[i] - stockHolding[i-1][j] * priceMat[i][j] * (1-transFeeRate)) < 1e-10:
                        actionMat.append([i, j, position, stockHolding[i-1][j] * priceMat[i][j]])
                        position = j
                        break
    
    if position != -1:
        actionMat.append([0, -1, position, cash])
    
    actionMat.reverse()
    return actionMat

# An approach that allow consecutive K days to hold all cash without any stocks    
def myAction03(priceMat, transFeeRate, K):
    """
    Trading strategy function that determines optimal trading actions based on price matrix.
    
    Args:
        priceMat: Price matrix for stocks over time
        transFeeRate: Transaction fee rate
        K: Period length for analysis
        
    Returns:
        actionMat: List of trading actions, each containing [day, from_pos, to_pos, amount]
    """
    import numpy as np
    
    totalDays, stockCount = priceMat.shape
    cash = 1000
    actionMat = []
    
    # Initialize holdings arrays
    stockHolding = np.zeros((totalDays, stockCount))
    cashHolding = np.zeros(totalDays)
    cashHolding[0] = cash
    
    # Initialize first day stock holdings
    stockHolding[0] = cash * (1 - transFeeRate) / priceMat[0]
    
    def update_holdings(day):
        """Update cash and stock holdings for given day"""
        # Update cash position
        cashHolding[day] = cashHolding[day-1]
        for stock in range(stockCount):
            possible_cash = stockHolding[day-1][stock] * priceMat[day][stock] * (1-transFeeRate)
            cashHolding[day] = max(cashHolding[day], possible_cash)
        
        # Update stock positions
        for stock in range(stockCount):
            buy_from_prev_cash = cashHolding[day-1] * (1-transFeeRate) / priceMat[day][stock]
            buy_from_curr_cash = cashHolding[day] * (1-transFeeRate) / priceMat[day][stock]
            stockHolding[day][stock] = max(stockHolding[day-1][stock], 
                                         buy_from_prev_cash,
                                         buy_from_curr_cash)
    
    # First pass: Calculate optimal holdings
    for day in range(1, totalDays):
        update_holdings(day)
    
    # Find period with minimum earnings rate
    min_earning_rate = float('inf')
    min_start_idx = 0
    
    for i in range(K, totalDays):
        earning_rate = (cashHolding[i] - cashHolding[i-K]) / cashHolding[i-K]
        if earning_rate < min_earning_rate:
            min_earning_rate = earning_rate
            min_start_idx = i-K
    
    # Second pass: Apply cash holding period constraint
    for day in range(1, totalDays):
        if min_start_idx <= day < min_start_idx + K:
            # Force cash holding during minimum earning period
            cashHolding[day] = cashHolding[day-1]
            if day == min_start_idx:
                # Sell all stocks
                for stock in range(stockCount):
                    possible_cash = stockHolding[day-1][stock] * priceMat[day][stock] * (1-transFeeRate)
                    cashHolding[day] = max(cashHolding[day], possible_cash)
                stockHolding[day] = 0
            elif day == min_start_idx + K:
                # Reinvest in stocks
                stockHolding[day] = cashHolding[day-1] * (1-transFeeRate) / priceMat[day]
            else:
                stockHolding[day] = 0
        else:
            update_holdings(day)
    
    # Backtrace to generate action matrix
    position = -1  # -1 represents cash position
    
    for day in range(totalDays-1, 0, -1):
        if position == -1:  # Currently in cash
            if cashHolding[day] != cashHolding[day-1]:
                for stock in range(stockCount):
                    if abs(cashHolding[day] - stockHolding[day-1][stock] * priceMat[day][stock] * (1-transFeeRate)) < 1e-10:
                        actionMat.append([day, stock, -1, stockHolding[day-1][stock] * priceMat[day][stock]])
                        position = stock
                        break
        else:  # Currently in stock
            if abs(stockHolding[day][position] - cashHolding[day-1] * (1-transFeeRate) / priceMat[day][position]) < 1e-10:
                actionMat.append([day, -1, position, cashHolding[day-1]])
                position = -1
            elif abs(stockHolding[day][position] - cashHolding[day] * (1-transFeeRate) / priceMat[day][position]) < 1e-10:
                for stock in range(stockCount):
                    if abs(cashHolding[day] - stockHolding[day-1][stock] * priceMat[day][stock] * (1-transFeeRate)) < 1e-10:
                        actionMat.append([day, stock, position, stockHolding[day-1][stock] * priceMat[day][stock]])
                        position = stock
                        break
    
    # Add initial action if needed
    if position != -1:
        actionMat.append([0, -1, position, cash])
    
    actionMat.reverse()
    return actionMat