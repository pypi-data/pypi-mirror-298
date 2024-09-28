from .tools.sec.sec_edgar_search import edgar_search_report

from .tools.sec.sec_10_k_8_k_filings import large_filing_module

from .tools.sec.llm_code_generator import generate_sovai_code

from .tools.sec.graphs import analyze_10k_graph



def sec_search(search="CFO Resgination"):

    return edgar_search_report(search)




def sec_filing(ticker="AAPL", form="10-Q", date_input="2023-Q3", verbose=False):

    return large_filing_module(ticker, form=form, date_input=date_input, verbose=verbose)



def code(prompt="get bankruptcy data for Tesla", verbose=False, run=False):

    return generate_sovai_code(prompt, verbose=verbose, run=run)



def sec_graph(ticker="AAPL", date_input="2024-Q3", verbose=False, ontology_type="causal", oai_model="gpt-4o-mini", batch=True, batch_size=10, sentiment_filter=None, output_dir="./docs", use_cache=True):

    return analyze_10k_graph(ticker, date_input, section_select=True, ontology_type=ontology_type, oai_model=oai_model, batch=batch, batch_size=batch_size, sentiment_filter=sentiment_filter, output_dir=output_dir, use_cache=use_cache, verbose=verbose)