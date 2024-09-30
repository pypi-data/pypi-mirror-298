import numpy as np
import pandas as pd
import anndata
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import os
import scanpy as sc
from scipy import sparse
import squidpy as sq
import warnings
import time
from tqdm import tqdm

warnings.filterwarnings("ignore")

def load_adata(adata_path):
    adata = sc.read_h5ad(adata_path)
    return adata

def process_qc(adata, save_path):
    img_path = os.path.join(save_path, 'images')
    if not os.path.exists(img_path):
        os.makedirs(img_path)

    print("Performing quality control...")
    start_time = time.time()

    # 1. quality control index (before filtering) --> 1 png
    fig, axs = plt.subplots(1, 2, figsize=(15, 4))
    sns.histplot(adata.obs["total_counts"], kde=False, ax=axs[0])
    sns.histplot(adata.obs["n_genes_by_counts"], kde=False, bins=60, ax=axs[1])
    axs[0].set_title("Total counts per cell", fontsize=15)
    axs[1].set_title("Number of genes per cell", fontsize=15)
    plt.savefig(os.path.join(img_path, 'qc_before_filtering.png'), bbox_inches='tight')

    # 6. quality control index (after filtering) --> 1 png
    fig, axs = plt.subplots(1, 2, figsize=(15, 4))
    sns.histplot(adata.obs["total_counts"], kde=False, ax=axs[0])

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Quality control completed in {elapsed_time:.2f} seconds.")

def process_leiden(adata, save_path, leiden_key='leiden',resolution=1.0):
    img_path = os.path.join(save_path, 'images')
    data_path = os.path.join(save_path, 'data_front')
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    print("Performing Leiden clustering...")
    start_time = time.time()

    # Re-run Leiden clustering with the specified key
    sc.tl.leiden(adata, key_added=leiden_key,resolution=resolution)

    # 2. leiden --> 1 png, 1 parquet
    plt.rcParams["figure.figsize"] = (12, 12)
    sc.pl.umap(adata, color=[leiden_key])
    plt.savefig(os.path.join(img_path, 'leiden.png'), bbox_inches='tight')

    umap_info = pd.DataFrame(adata.obsm['X_umap'], columns=['UMAP1', 'UMAP2'])
    umap_info.index = adata.obs.index
    umap_info[leiden_key] = adata.obs[leiden_key]
    umap_info['id'] = adata.obs.index
    umap_info.to_parquet(os.path.join(data_path, f'umap_{leiden_key}.parquet'))

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Leiden clustering completed in {elapsed_time:.2f} seconds.")

def process_hvg(adata, save_path,leiden_key='leiden'):
    img_path = os.path.join(save_path, 'images')
    data_path = os.path.join(save_path, 'data_front')
    download_path = os.path.join(save_path, 'data_download')
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    print("Identifying highly variable genes...")
    start_time = time.time()

    # 3. HVG --> 1 png, 1 svg, 1 html, 1 json, 1 csv
    sc.tl.rank_genes_groups(adata, leiden_key, method="t-test")
    sc.tl.dendrogram(adata, groupby=leiden_key)

    dot_p = sc.pl.rank_genes_groups_dotplot(adata, return_fig=True)
    dot_p.savefig(os.path.join(img_path, 'HVG_dotplot.png'), bbox_inches='tight')
    dot_p.savefig(os.path.join(download_path, 'HVG_dotplot.svg'), bbox_inches='tight')

    dot_color_df = dot_p.dot_color_df
    dot_size_df = dot_p.dot_size_df

    categories_idx_ordered = [i for i in list(dot_size_df.index)]

    genes = dot_size_df.columns.tolist()
    clusters = dot_size_df.index.tolist()

    min_value = dot_size_df.min().min()
    max_value = dot_size_df.max().max()

    # -----------------HVG_dotplot-----------------
    def calculate_size(value, min_size=5, max_size=25):
        return min_size + (value - min_value) / (max_value - min_value) * (max_size - min_size)

    fig = go.Figure()

    original_values = dot_size_df.values.ravel().tolist()

    for i, cluster in enumerate(tqdm(clusters, desc="Processing clusters", unit="cluster")):
        fig.add_trace(go.Scatter(
            x=list(range(len(genes))),
            y=[i] * len(genes),
            mode='markers',
            name=f'Cluster {cluster}',
            marker=dict(
                size=calculate_size(dot_size_df.loc[cluster]),
                color=dot_color_df.loc[cluster],
                colorscale='Viridis',
                showscale=i == 0,
                colorbar=dict(
                    title='Expression Level',
                    len=0.5,
                    y=0.75,
                    yanchor='top'
                ),
                sizemode='diameter',
            ),
            showlegend=False,
            customdata=original_values,
            hovertemplate='Cluster: %{y}<br>Gene: %{x}<br>Gene Fraction: %{customdata:.2f}<extra></extra>'
        ))

    # 添加横线和文字标注
    shapes = []
    annotations = []
    # 获取每个聚类的前 10 个高变基因
    top_genes_per_cluster = {}
    for cluster in clusters:
        start = clusters.index(cluster) * 10
        end = start + 10
        top_genes = genes[start:end]
        top_genes_per_cluster[cluster] = top_genes

    annotations = []
    for i, category in enumerate(tqdm(categories_idx_ordered, desc="Processing annotations", unit="annotation")):
        start = i * 10
        end = (i + 1) * 10
        shapes.append(dict(
            type="line",
            x0=start, x1=end - 1, y0=1.02, y1=1.02,
            xref='x', yref='paper',
            line=dict(color="Black", width=3)
        ))
        top_genes = top_genes_per_cluster[category]
        top_genes_str = '<br>'.join(top_genes)
        annotations.append(dict(
            x=(start + end - 1) / 2,y=1.05,
            xref='x', yref='paper',
            text=f'Cluster {category}',
            showarrow=False,
            font=dict(size=15),
            hovertext=f'High Variable Genes:<br>{top_genes_str}'
        ))

    fig.update_layout(
        xaxis=dict(
            title='Genes',
            tickmode='array',
            tickvals=list(range(len(genes))),
            ticktext=genes,
            tickangle=45,
            range=[-1, len(genes)]
        ),
        yaxis=dict(
            title='Clusters',
            tickmode='array',
            tickvals=list(range(len(clusters))),
            ticktext=clusters,
            range=[-0.5, len(clusters) - 0.5]
        ),
        height=1000,
        width=3000,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.22,
            xanchor="left",
            x=1.02,
            itemsizing='constant',
        ),
        margin=dict(t=100, b=100, l=50, r=150),
        shapes=shapes,
        annotations=annotations
    )

    # 保存成json和html
    fig.write_json(os.path.join(data_path, 'HVG_dotplot.json'))
    fig.write_html(os.path.join(data_path, 'HVG_dotplot.html'))

    # -----------------HVG_info-----------------
    gene_df = pd.DataFrame(adata.uns['rank_genes_groups']['names'])
    pval_df = pd.DataFrame(adata.uns['rank_genes_groups']['pvals'])
    pval_adj_df = pd.DataFrame(adata.uns['rank_genes_groups']['pvals_adj'])
    logfold_df = pd.DataFrame(adata.uns['rank_genes_groups']['logfoldchanges'])

    genes = []
    clusters = []
    pvals = []
    pvals_adj = []
    logfoldchanges = []

    # 提取每个聚类标签的前1000个基因
    for i in tqdm(range(0, len(gene_df.columns)), desc="Extracting genes", unit="cluster"):
        genes.extend(gene_df[str(i)][:100])
        pvals.extend(pval_df[str(i)][:100])
        pvals_adj.extend(pval_adj_df[str(i)][:100])
        logfoldchanges.extend(logfold_df[str(i)][:100])
        clusters.extend([str(i)] * min(len(gene_df[str(i)]), 100))

    # 创建新的 DataFrame
    result_df = pd.DataFrame({'names': genes, 'pvals': pvals, 'pvals adj': pvals_adj, 'logfoldchanges': logfoldchanges, 'cluster': clusters})

    # 定义一个函数，将值转换为科学计数法格式
    def to_scientific(x):
        if isinstance(x, float) or isinstance(x, int):
            return f"{x:.6e}"
        return x

    # 将数据框中的数值列转换为科学计数法格式
    df = result_df.applymap(to_scientific)

    # 保存数据框
    df.to_csv(os.path.join(data_path, 'HVG_info.csv'))

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Highly variable gene identification completed in {elapsed_time:.2f} seconds.")

def process_co_occurrence(adata, save_path,leiden_key='leiden'):
    img_path = os.path.join(save_path, 'images')
    if not os.path.exists(img_path):
        os.makedirs(img_path)

    print("Analyzing co-occurrence...")
    start_time = time.time()

    # 4. co_occurrence --> 1 png for each cluster
    adata_subsample = sc.pp.subsample(adata, fraction=0.5, copy=True)
    sq.gr.co_occurrence(
        adata_subsample,
        cluster_key=leiden_key,
    )
    for i in tqdm(adata.obs[leiden_key].unique(), desc="Processing clusters", unit="cluster"):
        sq.pl.co_occurrence(
            adata_subsample,
            cluster_key=leiden_key,
            clusters=i,
            figsize=(8, 8),
        )
        plt.savefig(os.path.join(img_path, f'co_occurrence_{i}.png'), bbox_inches='tight')
        plt.clf()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Co-occurrence analysis completed in {elapsed_time:.2f} seconds.")

def process_nhood_enrichment(adata, save_path,leiden_key='leiden'):
    img_path = os.path.join(save_path, 'images')
    download_path = os.path.join(save_path, 'data_download')
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    print("Analyzing neighborhood enrichment...")
    start_time = time.time()

    # 5. spatial_neighbors enrichment --> 1 png
    sq.gr.spatial_neighbors(adata, coord_type="generic", delaunay=True)
    sq.gr.centrality_scores(adata, cluster_key=leiden_key)
    sq.gr.nhood_enrichment(adata, cluster_key=leiden_key)

    sq.pl.nhood_enrichment(
        adata,
        cluster_key=leiden_key,
        figsize=(10, 10),
        title="Neighborhood enrichment adata",
    )
    plt.savefig(os.path.join(img_path, 'nhood_enrichment.png'), bbox_inches='tight')
    plt.savefig(os.path.join(download_path, 'nhood_enrichment.svg'), bbox_inches='tight')

    sq.gr.spatial_neighbors(adata, coord_type="generic", delaunay=True)
    sq.gr.spatial_autocorr(
        adata,
        mode="moran",
        n_perms=100,
        n_jobs=1,
    )
    adata.uns["moranI"]

    sq.gr.spatial_autocorr(
        adata,
        mode="moran",
        n_perms=100,
        n_jobs=1,
    )
    adata.uns["moranI"]

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Neighborhood enrichment analysis completed in {elapsed_time:.2f} seconds.")

def process_metadata(adata, save_path):
    data_path = os.path.join(save_path, 'data_front')
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    print("Saving metadata...")
    start_time = time.time()

    # 7. metadata --> 2 parquet, 1 npz
    adata.obs.to_parquet(os.path.join(data_path, 'cell_info.parquet'))
    adata.var.to_parquet(os.path.join(data_path, 'gene_info.parquet'))
    sparse.save_npz(os.path.join(data_path, 'adata_X.npz'), adata.X)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Metadata saved in {elapsed_time:.2f} seconds.")

def process_adata(adata, save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    print("Processing adata object...")
    start_time = time.time()

    process_qc(adata, save_path)
    process_leiden(adata, save_path)
    process_hvg(adata, save_path)
    process_co_occurrence(adata, save_path)
    process_nhood_enrichment(adata, save_path)
    process_metadata(adata, save_path)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"All processing steps completed in {elapsed_time:.2f} seconds.")

    return [adata, save_path]

def estimate_remaining_time(current_step, total_steps, elapsed_time):
    remaining_steps = total_steps - current_step
    if remaining_steps > 0:
        avg_step_time = elapsed_time / current_step
        remaining_time = avg_step_time * remaining_steps
        return remaining_time
    else:
        return 0

def main(adata_path, work_path, process_type, platform, all_steps, qc, leiden, hvg, co_occurrence, nhood_enrichment, save_metadata):
    adata = load_adata(adata_path)
    save_path = os.path.join(work_path, 'results')

    total_steps = sum([all_steps, qc, leiden, hvg, co_occurrence, nhood_enrichment, save_metadata])
    current_step = 0
    start_time = time.time()

    if all_steps or qc:
        process_qc(adata, save_path)
        current_step += 1
        remaining_time = estimate_remaining_time(current_step, total_steps, time.time() - start_time)
        print(f"Estimated remaining time: {remaining_time:.2f} seconds")

    if all_steps or leiden:
        process_leiden(adata, save_path)
        current_step += 1
        remaining_time = estimate_remaining_time(current_step, total_steps, time.time() - start_time)
        print(f"Estimated remaining time: {remaining_time:.2f} seconds")

    if all_steps or hvg:
        process_hvg(adata, save_path)
        current_step += 1
        remaining_time = estimate_remaining_time(current_step, total_steps, time.time() - start_time)
        print(f"Estimated remaining time: {remaining_time:.2f} seconds")

    if all_steps or co_occurrence:
        process_co_occurrence(adata, save_path)
        current_step += 1
        remaining_time = estimate_remaining_time(current_step, total_steps, time.time() - start_time)
        print(f"Estimated remaining time: {remaining_time:.2f} seconds")

    if all_steps or nhood_enrichment:
        process_nhood_enrichment(adata, save_path)
        current_step += 1
        remaining_time = estimate_remaining_time(current_step, total_steps, time.time() - start_time)
        print(f"Estimated remaining time: {remaining_time:.2f} seconds")

    if all_steps or save_metadata:
        process_metadata(adata, save_path)
        current_step += 1
        remaining_time = estimate_remaining_time(current_step, total_steps, time.time() - start_time)
        print(f"Estimated remaining time: {remaining_time:.2f} seconds")

    return [adata, save_path]