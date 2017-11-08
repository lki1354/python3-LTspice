from IPython.display import Markdown,Latex, display
def printmd(string):
    display(Markdown(string))


def displayEfficiencies(toShow):
    table = '| Konverter Type | Effizienz [%] |\n'
    table += '| --- | --- | \n'
    for name , converter in toShow.items():
        table += '|'+name+'| %3.2f | \n'%converter.efficiency_percent
    printmd(table)

def displayResults(toShow):
    table = '| Konverter Type | Effizienz [%] |dIout [mA] |dUout [mV]|Iout [A] |Uout [V]|dIin [A] |\n'
    table += '| --- | --- | --- | --- | --- | --- | \n'
    for converter in toShow:
        table += '|'+converter.name+'|%3.0f | %3.2f | %3.2f| %.3f |%.3f| %.3f |  \n'%converter.getValues()
    printmd(table)
    
def displayResultsTEX(toShow):
    table = 'Konverter Type & Eff. [\%] & dIout [mA] &dUout [mV]&Iout [A] &Uout [V]&dIin [A] \\\\ \hline \n'
    for converter in toShow:
        table += ''+converter.name+'& %3.2f & %3.2f & %3.2f & %.3f & %.3f & %.3f \\\\ \n'%converter.getValues()
    #display(Latex(table.replace('.',',')))
    print(table.replace('.',','))