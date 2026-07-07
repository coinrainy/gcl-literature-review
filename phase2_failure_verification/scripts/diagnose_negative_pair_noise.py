from __future__ import annotations

import argparse

import numpy as np

from utils import (
    batch_negative_collision,
    degree_group_masks,
    degree_vector,
    hard_negative_collision,
    homophily_group_masks,
    infer_num_nodes,
    load_graph_data,
    local_node_homophily,
    read_array,
    set_random_seed,
    setup_logger,
    unique_undirected_edges,
    write_csv_rows,
)


FIELDNAMES = [
    "dataset",
    "source",
    "augmentation_type",
    "augmentation_rate",
    "diagnostic_type",
    "group",
    "batch_size",
    "top_k",
    "total_negative_pairs",
    "same_class_negative_pairs",
    "false_negative_rate",
    "hard_negative_same_class_rate",
    "hard_negative_cross_class_rate",
    "hard_negative_false_negative_rate",
    "anchors_evaluated",
    "embedding_source",
    "labels_posthoc_only",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Diagnose batch and hard-negative false negative noise.")
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--data-root", default="data")
    parser.add_argument("--npz-path", default=None)
    parser.add_argument("--edge-index-path", default=None)
    parser.add_argument("--features-path", default=None)
    parser.add_argument("--labels-path", default=None)
    parser.add_argument("--batch-sizes", nargs="+", default=["128", "256", "512", "1024"])
    parser.add_argument("--num-batches", type=int, default=50)
    parser.add_argument("--top-k", nargs="+", type=int, default=[5, 10, 20, 50])
    parser.add_argument("--embedding-path", default=None)
    parser.add_argument("--max-nodes-for-hard-negative", type=int, default=5000)
    parser.add_argument("--augmentation-type", default="not_conditioned")
    parser.add_argument("--augmentation-rate", default="")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--output",
        default="phase2_failure_verification/outputs/tables/negative_pair_noise.csv",
    )
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--log-path", default=None)
    return parser.parse_args()


def _parse_batch_sizes(values):
    parsed = []
    for value in values:
        parsed.append("full" if str(value).lower() == "full" else int(value))
    return parsed


def main() -> None:
    args = parse_args()
    set_random_seed(args.seed)
    logger = setup_logger(log_path=args.log_path)
    graph = load_graph_data(
        args.dataset,
        data_root=args.data_root,
        edge_index_path=args.edge_index_path,
        features_path=args.features_path,
        labels_path=args.labels_path,
        npz_path=args.npz_path,
    )
    if graph.labels is None:
        raise ValueError("Negative pair diagnostics require labels for post-hoc collision analysis.")

    edges = unique_undirected_edges(graph.edge_index)
    num_nodes = infer_num_nodes(graph.edge_index, graph.features, graph.labels)
    local_h = local_node_homophily(num_nodes, edges, graph.labels)
    degree = degree_vector(num_nodes, edges)
    group_masks = {}
    group_masks.update(homophily_group_masks(local_h))
    group_masks.update(degree_group_masks(degree))

    rows = batch_negative_collision(
        graph.labels,
        batch_sizes=_parse_batch_sizes(args.batch_sizes),
        num_batches=args.num_batches,
        seed=args.seed,
        group_masks=group_masks,
    )

    embedding_source = ""
    embeddings = None
    if args.embedding_path:
        embeddings = read_array(args.embedding_path)
        embedding_source = "provided_embeddings"
    elif graph.features is not None:
        embeddings = graph.features
        embedding_source = "raw_feature_proxy"

    if embeddings is not None:
        rows.extend(
            hard_negative_collision(
                embeddings,
                graph.labels,
                top_k_values=args.top_k,
                seed=args.seed,
                group_masks=group_masks,
                max_nodes=args.max_nodes_for_hard_negative,
                embedding_source=embedding_source,
            )
        )
    else:
        logger.warning("No embeddings or features available; hard-negative diagnostics are skipped.")

    for row in rows:
        row["dataset"] = graph.name
        row["source"] = graph.source
        row["augmentation_type"] = args.augmentation_type
        row["augmentation_rate"] = args.augmentation_rate

    write_csv_rows(args.output, FIELDNAMES, rows, append=not args.overwrite)
    logger.info("Wrote negative pair diagnostics to %s", args.output)


if __name__ == "__main__":
    main()

