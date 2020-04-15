       
def readfile():
    quotes = []
    with open('quotes.txt') as fp:
        line = fp.readline()
        while line:
            string = ''
            while line:
                if line[0] != '-':
                    if line[0] != ' ':
                        string = string + line
                    line = fp.readline()
                else:
                    line = fp.readline()
                    break
            quotes.append(string)
    return quotes
