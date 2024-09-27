from .tools.sec.sec_edgar_search import edgar_search_report

from .tools.sec.sec_10_k_8_k_filings import large_filing_module

from .tools.sec.llm_code_generator import generate_sovai_code



def sec_search(search="CFO Resgination"):

    return edgar_search_report(search)




def sec_filing(ticker="AAPL", form="10-Q", date_input="2023-Q3", verbose=False):

    return large_filing_module(ticker, form=form, date_input=date_input, verbose=verbose)



def code(prompt="get bankruptcy data for Tesla", verbose=False, run=False):

    return generate_sovai_code(prompt, verbose=verbose, run=run)



