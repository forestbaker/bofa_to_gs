# Convert csv file from BofA to GS format
# 
# Written for Python 2.6 by Forest Baker
#
# 1.0	  3-15-09	creating skeleton
# 1.1   3-28-09 ditched using csv module, got the dict created, able to
#               call specific keys in to variables for display, removed
#               the : from time variable and converted buy/sell to 1/2.
# 1.2   3-29-09 Got the data formated correctly, but needed clarification
#               on some issues between the template and the sample file.
#				        Made sure the price and shares were 19 spaces in length
# 1.3   3-30-09 Removed extra spaces in the data and in the header fields
#               Added the variables per jmicelli's answer
#		            Figured out how to truncate the name of the exchange
# 1.4   4-01-09 Truncated the TradeID to last 4 characters
#
##############################################################################

import fileinput

FileIn = fileinput.input()
titles = FileIn.next().replace(" ","").split(',')
output = open("c:\\ftp_temp\\company_daytrading.txt", "w")

for row in FileIn:
    values = row.replace(" ","").split(',')
    data = dict(zip(titles, values))

# Make sure shares were executed
    if int(data['ExeShares']) > 0:
        Date = data['Date']        
        Account = data['Account']
        Broker = "BofA"
        Blank4 = "    "
        Blank2 = "  "

# Remove proceeding characters until last four remain
        TradeIdSize = len(data['ECNExecID'])
        while TradeIdSize > 4:
            rawTradeId = data['ECNExecID']
            TradeId = rawTradeId[1:]
            data['ECNExecID'] = TradeId
            TradeIdSize -= 1
            
# Remove trailing characters until the first two remain to abbreviate exchange name
        RouteSize = len(data['Route'])
        while RouteSize > 2:
            rawRoute = data['Route']
            Route = rawRoute[:-1]
            data['Route'] = Route
            RouteSize -= 1
        
# Left justify the symbol field with a width of 9, fill extra space with blanks
        Symbol = data['Symbol'].ljust(9)

# Prepend 0's to ExeShares until field length is 19
        ExeShares = data['ExeShares'].zfill(19)
        
# Create 4 decimal places filled with 0's after a period, add 0's until field length is 19 
        ExePrice = "%.4f" % float(data['ExePrice'])
        ExePrice = ExePrice.zfill(19)

# Change SELL/BUY to 1 or 2
        if data['Action'] == 'SELL-close':
            Action = 2
        else:
            Action = 1

# Remove : from time
        rawTime = data['Time']
        Time = rawTime.replace(":","")

# Format for Output to file
#        printf "%s\n" % (Date, Time, Account, Symbol, Route, Action, Blank4, Broker, Blank2, TradeId, ExeShares, ExePrice)
        output.write(Date)
        output.write(Time)
        output.write(Account)
        output.write(Symbol)
        output.write(Route)
        output.write(str(Action))
        output.write(Blank4)
        output.write(Broker)
        output.write(Blank2)
        output.write(TradeId)
        output.write(ExeShares)
        output.write(ExePrice)
        output.write('\n')

output.close()
