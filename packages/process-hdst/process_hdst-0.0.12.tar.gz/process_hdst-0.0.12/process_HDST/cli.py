import argparse
import os
import anndata
import sys

def main():
    parser = argparse.ArgumentParser(description='Spatial Transcriptomics Data Preprocessing')
    parser.add_argument('adata_path', type=str, help='Path to the adata object')
    parser.add_argument('work_path', type=str, help='Path to the working directory')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('--leiden_key', type=str, help='Choose the specific key for Leiden clustering')
    parser.add_argument('--after_leiden', action='store_true', help='Perform processing steps after Leiden clustering')
    parser.add_argument('--leiden_resolution', type=float, default=1.0, help='Resolution for Leiden clustering')
    parser.add_argument('--all', action='store_true', help='Perform all processing steps')
    parser.add_argument('--qc', action='store_true', help='Perform quality control')
    parser.add_argument('--leiden', action='store_true', help='Perform Leiden clustering')
    parser.add_argument('--hvg', action='store_true', help='Identify highly variable genes')
    parser.add_argument('--co_occurrence', action='store_true', help='Analyze co-occurrence')
    parser.add_argument('--nhood_enrichment', action='store_true', help='Analyze neighborhood enrichment')
    parser.add_argument('--save_metadata', action='store_true', help='Save metadata')

    args = parser.parse_args()

    save_path = os.path.join(args.work_path, 'results')

    from process_HDST import load_adata, process_adata, process_qc, process_leiden, process_hvg, process_co_occurrence, process_nhood_enrichment, process_metadata
    adata = load_adata(args.adata_path)

    if args.all or any([args.qc, args.leiden, args.hvg, args.co_occurrence, args.nhood_enrichment, args.save_metadata]):
        print(f"Processing adata object from {args.adata_path}...")
        adata, _ = process_adata(adata, save_path)
    else:
        print("Please specify at least one processing option or use --all for all processing steps.")
        return

    if args.after_leiden:
        if args.leiden_key:
            print("Performing all processing steps after Leiden clustering...")
            process_hvg(adata, save_path, leiden_key=args.leiden_key)
            process_co_occurrence(adata, save_path, leiden_key=args.leiden_key)
            process_nhood_enrichment(adata, save_path, leiden_key=args.leiden_key)
            process_metadata(adata, save_path)
            print("All processing steps after Leiden clustering completed successfully.")
        else:
            print("Please specify the Leiden key using --leiden_key.")
            return

    if args.all:
        print("Performing all processing steps...")
        process_qc(adata, save_path)
        try:
            process_leiden(adata, save_path, leiden_key=args.leiden_key, resolution=args.leiden_resolution)
        except Exception as e:
            print(f"Error occurred during Leiden clustering: {e}")
            print("Using default parameters for Leiden clustering: key is leiden, resolution is 1.0.")
            process_leiden(adata, save_path)
        process_hvg(adata, save_path, leiden_key=args.leiden_key)
        process_co_occurrence(adata, save_path, leiden_key=args.leiden_key)
        process_nhood_enrichment(adata, save_path, leiden_key=args.leiden_key)
        process_metadata(adata, save_path)
        print("All processing steps completed successfully.")

    else:
        if args.qc:
            print("Performing quality control...")
            process_qc(adata, save_path)
            print("Quality control completed successfully.")

        if args.leiden:
            print("Performing Leiden clustering...")
            try:
                process_leiden(adata, save_path, leiden_key=args.leiden_key, resolution=args.leiden_resolution)
            except Exception as e:
                print(f"Error occurred during Leiden clustering: {e}")
                print("Using default parameters for Leiden clustering.")
                process_leiden(adata, save_path)
            print("Leiden clustering completed successfully.")

        if args.hvg:
            print("Identifying highly variable genes...")
            process_hvg(adata, save_path, leiden_key=args.leiden_key)
            print("Highly variable gene identification completed successfully.")

        if args.co_occurrence:
            print("Analyzing co-occurrence...")
            process_co_occurrence(adata, save_path, leiden_key=args.leiden_key)
            print("Co-occurrence analysis completed successfully.")

        if args.nhood_enrichment:
            print("Analyzing neighborhood enrichment...")
            process_nhood_enrichment(adata, save_path, leiden_key=args.leiden_key)
            print("Neighborhood enrichment analysis completed successfully.")

        if args.save_metadata:
            print("Saving metadata...")
            process_metadata(adata, save_path)
            print("Metadata saved successfully.")

if __name__ == '__main__':
    main()