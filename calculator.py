class THORChain_Calculator():
    
    def __init__(self, **kwargs):
        self.Trade_size = kwargs['Trade_size']
        self.Input_Asset_Liquidity = kwargs['Input_Asset_Liquidity']
        self.RUNE1 = kwargs['RUNE1']
        self.RUNE2 = kwargs['RUNE2']
        self.Output_Asset_Liquidity = kwargs['Output_Asset_Liquidity']
        self.Input_Asset_fee = kwargs['Input_Asset_fee']
        self.Output_Asset_fee = kwargs['Output_Asset_fee']
        self.Network_fee = kwargs['Network_fee']
        
    
    def calculate(self, Q):
        self.total_flat_fee = 0
        self.total_slip_fee = 0
        self.total_fee = 0
        self.total_output = 0
        
        Input_Asset_Liquidity_1Trade = self.Input_Asset_Liquidity
        Input_Asset_Liquidity_2Trade = self.RUNE2

        Output_Asset_Liquidity_1Trade = self.RUNE1
        Output_Asset_Liquidity_2Trade = self.Output_Asset_Liquidity
        print(Q, 'Transaction')
        for i in range(Q):
            print('Round ', i+1)
            # 1st Trade (x-RUNE)
            # Inputs:
            Real_Input_1Trade = self.Trade_size/Q - self.Input_Asset_fee
            # Calculations:
            Start_Price = Input_Asset_Liquidity_1Trade / Output_Asset_Liquidity_1Trade # Start Price
            Output_Slip = Real_Input_1Trade / (Real_Input_1Trade + Input_Asset_Liquidity_1Trade) # Output Slip
            Output = Real_Input_1Trade*Output_Asset_Liquidity_1Trade / (Real_Input_1Trade + Input_Asset_Liquidity_1Trade) # Output
            End_Price_1Trade = (Input_Asset_Liquidity_1Trade + Real_Input_1Trade) / (Output_Asset_Liquidity_1Trade - Output) # End Price
            Slip_Fee_1Trade = Output_Slip * Output # Slip Fee
            Tokens_Emitted = Output - Slip_Fee_1Trade # Tokens Emitted

            Input_Asset_Liquidity_1Trade = Real_Input_1Trade + Input_Asset_Liquidity_1Trade
            Output_Asset_Liquidity_1Trade = Output_Asset_Liquidity_1Trade - Output

            print(f'''1nd Trade (x-RUNE)
            Result: {Real_Input_1Trade:.7f} traded for {Tokens_Emitted:.2f}
            Final Exchange Rate {Real_Input_1Trade/Tokens_Emitted:.7f}
            Liquidity Fee %  {(Slip_Fee_1Trade/Output)*100:.2f}%
            ''')


            # 2nd Trade (RUNE-x)
            # Inputs
            Real_Input_2Trade = Tokens_Emitted - self.Network_fee
            # Calculations:
            Start_Price = Input_Asset_Liquidity_2Trade / Output_Asset_Liquidity_2Trade
            Output_Slip = Real_Input_2Trade / (Real_Input_2Trade + Input_Asset_Liquidity_2Trade)
            Output = Real_Input_2Trade * Output_Asset_Liquidity_2Trade / (Real_Input_2Trade + Input_Asset_Liquidity_2Trade) 
            End_Price_2Trade = (Input_Asset_Liquidity_2Trade + Real_Input_2Trade) / (Output_Asset_Liquidity_2Trade - Output)
            Slip_Fee_2Trade = Output_Slip * Output
            Transaction_fee = self.Output_Asset_fee
            Tokens_Emitted_2 = Output - Slip_Fee_2Trade - Transaction_fee
            self.total_output += Tokens_Emitted_2

            Input_Asset_Liquidity_2Trade = Real_Input_2Trade + Input_Asset_Liquidity_2Trade
            Output_Asset_Liquidity_2Trade = Output_Asset_Liquidity_2Trade - Output

            print(f'''2nd Trade (RUNE-x)
            Result: {Real_Input_2Trade:.7f} traded for {Tokens_Emitted_2:.2f}
            Final Exchange Rate {Real_Input_2Trade/Tokens_Emitted_2:.7f}
            Liquidity Fee % {(Slip_Fee_2Trade/Output)*100:.2f}%
            ''')


            # Result
            self.total_flat_fee += self.Input_Asset_fee/End_Price_1Trade/End_Price_2Trade + 1/End_Price_2Trade*self.Network_fee+Transaction_fee
            self.total_slip_fee += Slip_Fee_1Trade/End_Price_2Trade+Slip_Fee_2Trade


        
        self.total_fee = self.total_flat_fee + self.total_slip_fee
        print(f'''Result:
        {self.Trade_size:.4f} traded for {self.total_output:.2f}
        {self.total_flat_fee:.4f} total flat fee paid for trades {self.total_flat_fee*End_Price_1Trade*End_Price_2Trade:.4f}
        {self.total_slip_fee:.4f} total slip fee paid for trades {self.total_slip_fee/self.total_output*100:.3f}%
        {self.total_fee:.4f} total fee paid for trades {self.total_fee/self.total_output*100:.3f}%
        ''')
        
        self.total_slip_fee *= End_Price_1Trade*End_Price_2Trade
        self.total_flat_fee *= End_Price_1Trade*End_Price_2Trade
        
        return self.total_fee*End_Price_1Trade*End_Price_2Trade
        

def main():
    Input_Asset_Name = input('Input Asset Name: ')
    Output_Asset_Name = input('Output Asset Name: ')
    
    THORChain = THORChain_Calculator(Trade_size=float(input('Trade size ('+Input_Asset_Name+'): ')),
                                     Input_Asset_Liquidity= float(input(Input_Asset_Name+' Pool Liquidity ('+Input_Asset_Name+'): ')),
                                     RUNE1 = float(input(Input_Asset_Name+' Pool Liquidity (RUNE): ')),
                                     RUNE2 = float(input(Output_Asset_Name+' Pool Liquidity (RUNE): ')),
                                     Output_Asset_Liquidity = float(input(Output_Asset_Name+' Pool Liquidity ('+Output_Asset_Name+'): ')),
                                     Input_Asset_fee = float(input(Input_Asset_Name+' Transaction fee: ')),
                                     Output_Asset_fee = float(input(Output_Asset_Name+' Transaction fee: ')),
                                     Network_fee = float(input('Thorchain Network fee (RUNE): ')))
    print()
    total_fee_list = [] 
    Q = 1
    while True:

        total_fee  = THORChain.calculate(Q)

        if total_fee_list != [] and total_fee_list[len(total_fee_list)-1][1] < total_fee:
            total_fee = total_fee_list[len(total_fee_list)-1][1]
            Q -= 1
            break

        trade_size, total_output, total_slip_fee = THORChain.Trade_size, THORChain.total_output, THORChain.total_slip_fee
        total_fee_list.append([Q, total_fee])
        Q += 1

    print(f'''
    This trade should be executed in {Q} transactions of {trade_size/Q:.4f} {Input_Asset_Name}.
    This should result in a total {total_output:.4f} of {Output_Asset_Name} with a final exchange rate of {trade_size/total_output:.4f}.
    Total fee paid will be {total_fee:.4f} {Input_Asset_Name}.
    Out of which slip fee is {total_slip_fee:.4f} {Input_Asset_Name}
    '''
    )       

if __name__ == "__main__":
    main()
    
