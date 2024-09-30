from .afterPreprocess import load_adata, process_adata, process_qc, process_leiden, process_hvg, process_co_occurrence, process_nhood_enrichment, process_metadata
from .cli import main

if __name__ == '__main__':
    main()