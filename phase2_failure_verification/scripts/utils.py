from __future__ import annotations

import csv
import json
import logging
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np


@dataclass
class GraphData:
    name: str
    edge_index: np.ndarray
    features: Optional[np.ndarray]
    labels: Optional[np.ndarray]
    source: str


def setup_logger(name: str = "phase2", log_path: Optional[str] = None) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    stream = logging.StreamHandler()
    stream.setFormatter(formatter)
    logger.addHandler(stream)
    if log_path:
        Path(log_path).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger


def set_random_seed(seed: int) -> np.random.Generator:
    random.seed(seed)
    np.random.seed(seed)
    return np.random.default_rng(seed)


def normalize_edge_index(edge_index: np.ndarray) -> np.ndarray:
    edge_index = np.asarray(edge_index)
    if edge_index.ndim != 2:
        raise ValueError("edge_index must be a 2D array with shape [2, E] or [E, 2].")
    if edge_index.shape[0] == 2:
        normalized = edge_index
    elif edge_index.shape[1] == 2:
        normalized = edge_index.T
    else:
        raise ValueError("edge_index must have shape [2, E] or [E, 2].")
    return normalized.astype(np.int64, copy=False)


def unique_undirected_edges(edge_index: np.ndarray, remove_self_loops: bool = True) -> np.ndarray:
    edge_index = normalize_edge_index(edge_index)
    if edge_index.shape[1] == 0:
        return np.empty((0, 2), dtype=np.int64)
    src = edge_index[0]
    dst = edge_index[1]
    if remove_self_loops:
        mask = src != dst
        src = src[mask]
        dst = dst[mask]
    lo = np.minimum(src, dst)
    hi = np.maximum(src, dst)
    edges = np.stack([lo, hi], axis=1)
    if edges.size == 0:
        return np.empty((0, 2), dtype=np.int64)
    return np.unique(edges, axis=0)


def infer_num_nodes(
    edge_index: np.ndarray,
    features: Optional[np.ndarray],
    labels: Optional[np.ndarray],
) -> int:
    candidates: List[int] = []
    if features is not None:
        candidates.append(int(features.shape[0]))
    if labels is not None:
        candidates.append(int(labels.shape[0]))
    if edge_index.size:
        candidates.append(int(edge_index.max()) + 1)
    if not candidates:
        raise ValueError("Cannot infer num_nodes from empty edges, features, and labels.")
    return max(candidates)


def read_array(path: str, dtype: Optional[np.dtype] = None) -> np.ndarray:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    if p.suffix.lower() == ".npy":
        arr = np.load(p, allow_pickle=False)
    elif p.suffix.lower() == ".npz":
        data = np.load(p, allow_pickle=False)
        key = "arr_0" if "arr_0" in data.files else data.files[0]
        arr = data[key]
    else:
        arr = np.loadtxt(p, delimiter=",")
    if dtype is not None:
        arr = arr.astype(dtype)
    return arr


def _load_custom_graph(
    dataset: str,
    edge_index_path: Optional[str],
    features_path: Optional[str],
    labels_path: Optional[str],
    npz_path: Optional[str],
) -> Optional[GraphData]:
    if npz_path:
        data = np.load(npz_path, allow_pickle=False)
        edge_key = "edge_index" if "edge_index" in data.files else "edges"
        feature_key = "x" if "x" in data.files else "features"
        label_key = "y" if "y" in data.files else "labels"
        if edge_key not in data.files:
            raise ValueError("Custom npz must contain edge_index or edges.")
        edges = normalize_edge_index(data[edge_key])
        features = data[feature_key] if feature_key in data.files else None
        labels = data[label_key].reshape(-1) if label_key in data.files else None
        return GraphData(dataset, edges, features, labels, f"custom_npz:{npz_path}")

    if not edge_index_path:
        return None

    edges = normalize_edge_index(read_array(edge_index_path, dtype=np.int64))
    features = read_array(features_path) if features_path else None
    labels = read_array(labels_path, dtype=np.int64).reshape(-1) if labels_path else None
    return GraphData(dataset, edges, features, labels, f"custom_edges:{edge_index_path}")


def _load_pyg_graph(dataset: str, data_root: str) -> GraphData:
    try:
        from torch_geometric.datasets import Actor, Amazon, Coauthor, Planetoid, WebKB, WikipediaNetwork
    except Exception as exc:
        raise RuntimeError(
            "PyG is not available. Use --npz-path or --edge-index-path/--features-path/--labels-path. "
            "Expected custom npz keys: edge_index or edges, optional x/features, optional y/labels."
        ) from exc

    name = dataset.strip()
    key = name.lower().replace("_", " ").replace("-", " ")
    root = Path(data_root)

    if key in {"cora", "citeseer", "pubmed"}:
        ds = Planetoid(root=str(root / "Planetoid" / name), name=name)
    elif key in {"amazon computers", "computers", "amazon computer"}:
        ds = Amazon(root=str(root / "Amazon"), name="Computers")
        name = "Amazon Computers"
    elif key in {"coauthor cs", "cs"}:
        ds = Coauthor(root=str(root / "Coauthor"), name="CS")
        name = "Coauthor CS"
    elif key in {"chameleon", "squirrel"}:
        try:
            ds = WikipediaNetwork(root=str(root / "WikipediaNetwork"), name=key.capitalize(), geom_gcn_preprocess=True)
        except TypeError:
            ds = WikipediaNetwork(root=str(root / "WikipediaNetwork"), name=key.capitalize())
        name = key.capitalize()
    elif key == "actor":
        ds = Actor(root=str(root / "Actor"))
        name = "Actor"
    elif key in {"cornell", "texas", "wisconsin"}:
        ds = WebKB(root=str(root / "WebKB"), name=key.capitalize())
        name = key.capitalize()
    else:
        raise RuntimeError(
            f"No built-in loader is defined for dataset '{dataset}'. "
            "Use custom npz or CSV/NumPy inputs for this dataset."
        )

    data = ds[0]
    edge_index = data.edge_index.detach().cpu().numpy()
    features = data.x.detach().cpu().numpy() if getattr(data, "x", None) is not None else None
    labels = data.y.detach().cpu().numpy().reshape(-1) if getattr(data, "y", None) is not None else None
    return GraphData(name=name, edge_index=edge_index, features=features, labels=labels, source="pyg")


def load_graph_data(
    dataset: str,
    data_root: str = "data",
    edge_index_path: Optional[str] = None,
    features_path: Optional[str] = None,
    labels_path: Optional[str] = None,
    npz_path: Optional[str] = None,
) -> GraphData:
    custom = _load_custom_graph(dataset, edge_index_path, features_path, labels_path, npz_path)
    if custom is not None:
        return custom
    return _load_pyg_graph(dataset, data_root)


def labels_are_available(labels: Optional[np.ndarray]) -> bool:
    return labels is not None and labels.size > 0


def valid_label_mask(labels: Optional[np.ndarray]) -> Optional[np.ndarray]:
    if labels is None:
        return None
    labels = np.asarray(labels)
    if np.issubdtype(labels.dtype, np.floating):
        return ~np.isnan(labels)
    return labels >= 0


def adjacency_from_edges(num_nodes: int, edges: np.ndarray) -> List[List[int]]:
    adj: List[List[int]] = [[] for _ in range(num_nodes)]
    for u, v in edges:
        if 0 <= u < num_nodes and 0 <= v < num_nodes:
            adj[int(u)].append(int(v))
            adj[int(v)].append(int(u))
    return adj


def degree_vector(num_nodes: int, edges: np.ndarray) -> np.ndarray:
    degree = np.zeros(num_nodes, dtype=np.float64)
    if edges.size == 0:
        return degree
    counts = np.bincount(edges.reshape(-1), minlength=num_nodes)
    degree[: len(counts)] = counts[:num_nodes]
    return degree


def class_distribution(labels: Optional[np.ndarray]) -> str:
    if labels is None:
        return "Unknown"
    mask = valid_label_mask(labels)
    values, counts = np.unique(labels[mask], return_counts=True)
    payload = {str(int(v)): int(c) for v, c in zip(values, counts)}
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def global_edge_homophily(edges: np.ndarray, labels: Optional[np.ndarray]) -> Tuple[float, int, int]:
    if labels is None or edges.size == 0:
        return math.nan, 0, 0
    mask = valid_label_mask(labels)
    same = 0
    total = 0
    for u, v in edges:
        if mask[u] and mask[v]:
            total += 1
            if labels[u] == labels[v]:
                same += 1
    if total == 0:
        return math.nan, 0, 0
    return same / total, same, total - same


def local_node_homophily(num_nodes: int, edges: np.ndarray, labels: Optional[np.ndarray]) -> np.ndarray:
    result = np.full(num_nodes, np.nan, dtype=np.float64)
    if labels is None:
        return result
    mask = valid_label_mask(labels)
    adj = adjacency_from_edges(num_nodes, edges)
    for node, neighbors in enumerate(adj):
        if not mask[node]:
            continue
        labeled_neighbors = [nbr for nbr in neighbors if mask[nbr]]
        if not labeled_neighbors:
            continue
        same = sum(1 for nbr in labeled_neighbors if labels[nbr] == labels[node])
        result[node] = same / len(labeled_neighbors)
    return result


def graph_statistics(graph: GraphData) -> Dict[str, object]:
    edges = unique_undirected_edges(graph.edge_index)
    num_nodes = infer_num_nodes(graph.edge_index, graph.features, graph.labels)
    degree = degree_vector(num_nodes, edges)
    local_h = local_node_homophily(num_nodes, edges, graph.labels)
    edge_h, same_edges, cross_edges = global_edge_homophily(edges, graph.labels)
    labeled_edges = same_edges + cross_edges
    num_classes = (
        int(np.unique(graph.labels[valid_label_mask(graph.labels)]).size)
        if graph.labels is not None
        else "Unknown"
    )
    return {
        "dataset": graph.name,
        "source": graph.source,
        "num_nodes": num_nodes,
        "num_edges": int(edges.shape[0]),
        "num_features": int(graph.features.shape[1]) if graph.features is not None and graph.features.ndim > 1 else 0,
        "num_classes": num_classes,
        "global_edge_homophily": edge_h,
        "local_node_homophily_mean": float(np.nanmean(local_h)) if np.isfinite(local_h).any() else math.nan,
        "local_node_homophily_std": float(np.nanstd(local_h)) if np.isfinite(local_h).any() else math.nan,
        "degree_mean": float(np.mean(degree)) if degree.size else math.nan,
        "degree_std": float(np.std(degree)) if degree.size else math.nan,
        "class_distribution": class_distribution(graph.labels),
        "same_class_edge_ratio": same_edges / labeled_edges if labeled_edges else math.nan,
        "cross_class_edge_ratio": cross_edges / labeled_edges if labeled_edges else math.nan,
        "labels_posthoc_only": True,
    }


def homophily_group_masks(local_h: np.ndarray) -> Dict[str, np.ndarray]:
    finite = np.isfinite(local_h)
    return {
        "low_homophily": finite & (local_h < 0.33),
        "medium_homophily": finite & (local_h >= 0.33) & (local_h < 0.66),
        "high_homophily": finite & (local_h >= 0.66),
    }


def degree_group_masks(degree: np.ndarray) -> Dict[str, np.ndarray]:
    if degree.size == 0:
        return {"low_degree": np.array([], dtype=bool), "high_degree": np.array([], dtype=bool)}
    median = float(np.median(degree))
    return {
        "low_degree": degree <= median,
        "high_degree": degree > median,
    }


def safe_mean(values: np.ndarray) -> float:
    values = np.asarray(values, dtype=np.float64)
    if values.size == 0 or not np.isfinite(values).any():
        return math.nan
    return float(np.nanmean(values))


def safe_std(values: np.ndarray) -> float:
    values = np.asarray(values, dtype=np.float64)
    if values.size == 0 or not np.isfinite(values).any():
        return math.nan
    return float(np.nanstd(values))


def drop_edges(edges: np.ndarray, rate: float, rng: np.random.Generator) -> np.ndarray:
    if edges.size == 0:
        return edges.copy()
    keep = rng.random(edges.shape[0]) >= rate
    return edges[keep]


def mask_features(features: np.ndarray, rate: float, rng: np.random.Generator, mode: str = "feature") -> np.ndarray:
    augmented = np.array(features, copy=True)
    if augmented.size == 0 or rate <= 0:
        return augmented
    if mode == "element":
        augmented[rng.random(augmented.shape) < rate] = 0
    else:
        num_features = augmented.shape[1] if augmented.ndim > 1 else 1
        num_mask = int(round(num_features * rate))
        if num_mask > 0:
            cols = rng.choice(num_features, size=min(num_mask, num_features), replace=False)
            if augmented.ndim == 1:
                augmented[cols] = 0
            else:
                augmented[:, cols] = 0
    return augmented


def edge_preservation_by_label(
    original_edges: np.ndarray,
    retained_edges: np.ndarray,
    labels: Optional[np.ndarray],
) -> Dict[str, object]:
    original_set = {tuple(edge) for edge in original_edges.tolist()}
    retained_set = {tuple(edge) for edge in retained_edges.tolist()}
    dropped_set = original_set - retained_set
    counts = {
        "retained_same_class_edges": 0,
        "retained_cross_class_edges": 0,
        "dropped_same_class_edges": 0,
        "dropped_cross_class_edges": 0,
    }
    if labels is None:
        counts.update(
            {
                "same_class_edge_retention_rate": math.nan,
                "cross_class_edge_retention_rate": math.nan,
                "labels_posthoc_only": True,
            }
        )
        return counts

    mask = valid_label_mask(labels)
    for edge_set, prefix in [(retained_set, "retained"), (dropped_set, "dropped")]:
        for u, v in edge_set:
            if not (mask[u] and mask[v]):
                continue
            relation = "same_class" if labels[u] == labels[v] else "cross_class"
            counts[f"{prefix}_{relation}_edges"] += 1

    same_total = counts["retained_same_class_edges"] + counts["dropped_same_class_edges"]
    cross_total = counts["retained_cross_class_edges"] + counts["dropped_cross_class_edges"]
    counts["same_class_edge_retention_rate"] = (
        counts["retained_same_class_edges"] / same_total if same_total else math.nan
    )
    counts["cross_class_edge_retention_rate"] = (
        counts["retained_cross_class_edges"] / cross_total if cross_total else math.nan
    )
    counts["labels_posthoc_only"] = True
    return counts


def _label_distribution(labels: np.ndarray, nodes: Sequence[int], classes: np.ndarray) -> np.ndarray:
    if len(nodes) == 0:
        return np.zeros(classes.size, dtype=np.float64)
    counts = np.zeros(classes.size, dtype=np.float64)
    class_to_idx = {int(label): idx for idx, label in enumerate(classes.tolist())}
    mask = valid_label_mask(labels)
    total = 0
    for node in nodes:
        if mask[node]:
            counts[class_to_idx[int(labels[node])]] += 1
            total += 1
    if total == 0:
        return counts
    return counts / total


def js_divergence(p: np.ndarray, q: np.ndarray) -> float:
    p = np.asarray(p, dtype=np.float64)
    q = np.asarray(q, dtype=np.float64)
    if p.sum() == 0 and q.sum() == 0:
        return 0.0
    if p.sum() > 0:
        p = p / p.sum()
    if q.sum() > 0:
        q = q / q.sum()
    m = 0.5 * (p + q)

    def kl(a: np.ndarray, b: np.ndarray) -> float:
        mask = a > 0
        return float(np.sum(a[mask] * np.log2(a[mask] / b[mask])))

    return 0.5 * kl(p, m) + 0.5 * kl(q, m)


def neighborhood_semantic_drift(
    num_nodes: int,
    original_edges: np.ndarray,
    augmented_edges: np.ndarray,
    labels: Optional[np.ndarray],
) -> Dict[str, np.ndarray]:
    if labels is None:
        nan = np.full(num_nodes, np.nan, dtype=np.float64)
        return {
            "neighbor_label_distribution_js_divergence": nan,
            "neighbor_label_distribution_l1_distance": nan,
            "local_homophily_change": nan,
        }
    classes = np.unique(labels[valid_label_mask(labels)])
    original_adj = adjacency_from_edges(num_nodes, original_edges)
    augmented_adj = adjacency_from_edges(num_nodes, augmented_edges)
    original_h = local_node_homophily(num_nodes, original_edges, labels)
    augmented_h = local_node_homophily(num_nodes, augmented_edges, labels)
    js_values = np.full(num_nodes, np.nan, dtype=np.float64)
    l1_values = np.full(num_nodes, np.nan, dtype=np.float64)
    for node in range(num_nodes):
        p = _label_distribution(labels, original_adj[node], classes)
        q = _label_distribution(labels, augmented_adj[node], classes)
        js_values[node] = js_divergence(p, q)
        l1_values[node] = float(np.abs(p - q).sum())
    return {
        "neighbor_label_distribution_js_divergence": js_values,
        "neighbor_label_distribution_l1_distance": l1_values,
        "local_homophily_change": augmented_h - original_h,
    }


def l2_normalize(matrix: np.ndarray) -> np.ndarray:
    matrix = np.asarray(matrix, dtype=np.float64)
    if matrix.ndim == 1:
        matrix = matrix.reshape(-1, 1)
    norm = np.linalg.norm(matrix, axis=1, keepdims=True)
    norm[norm == 0] = 1.0
    return matrix / norm


def positive_similarity_summary(
    view1: np.ndarray,
    view2: np.ndarray,
    labels: Optional[np.ndarray],
    group_masks: Dict[str, np.ndarray],
    threshold: Optional[float],
    max_rank_nodes: int,
    seed: int,
) -> Dict[str, Dict[str, object]]:
    rng = np.random.default_rng(seed)
    z1 = l2_normalize(view1)
    z2 = l2_normalize(view2)
    n = min(z1.shape[0], z2.shape[0])
    z1 = z1[:n]
    z2 = z2[:n]
    same_node_sim = np.sum(z1 * z2, axis=1)
    all_masks = {"all": np.ones(n, dtype=bool)}
    for key, mask in group_masks.items():
        all_masks[key] = np.asarray(mask[:n], dtype=bool)

    sampled = np.arange(n)
    if n > max_rank_nodes:
        sampled = np.sort(rng.choice(n, size=max_rank_nodes, replace=False))
    sim_matrix = z1[sampled] @ z2.T
    same_sampled = same_node_sim[sampled]
    ranks = 1 + np.sum(sim_matrix > same_sampled[:, None], axis=1)
    rank_full = np.full(n, np.nan, dtype=np.float64)
    rank_full[sampled] = ranks

    class_avg = np.full(n, np.nan, dtype=np.float64)
    if labels is not None:
        valid = valid_label_mask(labels)[:n]
        for label in np.unique(labels[:n][valid]):
            idx = np.where(valid & (labels[:n] == label))[0]
            if idx.size <= 1:
                continue
            sims = z1[idx] @ z2[idx].T
            class_avg[idx] = (sims.sum(axis=1) - np.diag(sims)) / (idx.size - 1)

    if threshold is not None:
        low_reliability = same_node_sim < threshold
    else:
        low_reliability = np.isfinite(class_avg) & (same_node_sim < class_avg)

    summary: Dict[str, Dict[str, object]] = {}
    for group, mask in all_masks.items():
        mask = mask[:n]
        if not mask.any():
            summary[group] = {
                "positive_pair_cosine_similarity": math.nan,
                "positive_pair_cosine_similarity_std": math.nan,
                "positive_pair_rank": math.nan,
                "positive_pair_similarity_drop": math.nan,
                "low_reliability_positive_ratio": math.nan,
                "positive_nodes_evaluated": 0,
            }
            continue
        similarity_drop = class_avg[mask] - same_node_sim[mask]
        summary[group] = {
            "positive_pair_cosine_similarity": safe_mean(same_node_sim[mask]),
            "positive_pair_cosine_similarity_std": safe_std(same_node_sim[mask]),
            "positive_pair_rank": safe_mean(rank_full[mask]),
            "positive_pair_similarity_drop": safe_mean(similarity_drop),
            "low_reliability_positive_ratio": float(np.mean(low_reliability[mask])),
            "positive_nodes_evaluated": int(mask.sum()),
        }
    return summary


def batch_negative_collision(
    labels: np.ndarray,
    batch_sizes: Sequence[int],
    num_batches: int,
    seed: int,
    group_masks: Dict[str, np.ndarray],
) -> List[Dict[str, object]]:
    rng = np.random.default_rng(seed)
    n = labels.shape[0]
    valid = valid_label_mask(labels)
    rows: List[Dict[str, object]] = []
    masks = {"all": valid.copy()}
    masks.update({name: np.asarray(mask, dtype=bool) & valid for name, mask in group_masks.items()})

    for batch_size in batch_sizes:
        effective_size = n if str(batch_size).lower() == "full" else min(int(batch_size), n)
        accum = {group: {"same": 0, "total": 0, "anchors": 0} for group in masks}
        for _ in range(num_batches):
            if effective_size == n:
                batch = np.arange(n)
            else:
                batch = rng.choice(n, size=effective_size, replace=False)
            batch_labels = labels[batch]
            same_matrix = batch_labels[:, None] == batch_labels[None, :]
            np.fill_diagonal(same_matrix, False)
            valid_matrix = valid[batch][:, None] & valid[batch][None, :]
            np.fill_diagonal(valid_matrix, False)
            for group, mask in masks.items():
                anchor_mask = mask[batch]
                if not anchor_mask.any():
                    continue
                group_valid = valid_matrix & anchor_mask[:, None]
                accum[group]["same"] += int((same_matrix & group_valid).sum())
                accum[group]["total"] += int(group_valid.sum())
                accum[group]["anchors"] += int(anchor_mask.sum())
        for group, values in accum.items():
            total = values["total"]
            same = values["same"]
            rows.append(
                {
                    "diagnostic_type": "batch_random",
                    "group": group,
                    "batch_size": effective_size,
                    "top_k": "",
                    "total_negative_pairs": total,
                    "same_class_negative_pairs": same,
                    "false_negative_rate": same / total if total else math.nan,
                    "hard_negative_same_class_rate": "",
                    "hard_negative_cross_class_rate": "",
                    "hard_negative_false_negative_rate": "",
                    "anchors_evaluated": values["anchors"],
                    "embedding_source": "",
                    "labels_posthoc_only": True,
                }
            )
    return rows


def hard_negative_collision(
    embeddings: np.ndarray,
    labels: np.ndarray,
    top_k_values: Sequence[int],
    seed: int,
    group_masks: Dict[str, np.ndarray],
    max_nodes: int,
    embedding_source: str,
) -> List[Dict[str, object]]:
    rng = np.random.default_rng(seed)
    n = min(embeddings.shape[0], labels.shape[0])
    selected = np.arange(n)
    if n > max_nodes:
        selected = np.sort(rng.choice(n, size=max_nodes, replace=False))
    z = l2_normalize(embeddings[:n][selected])
    y = labels[:n][selected]
    valid = valid_label_mask(y)
    sim = z @ z.T
    np.fill_diagonal(sim, -np.inf)
    masks = {"all": valid.copy()}
    for name, mask in group_masks.items():
        masks[name] = np.asarray(mask[:n], dtype=bool)[selected] & valid

    rows: List[Dict[str, object]] = []
    for top_k in top_k_values:
        k = min(int(top_k), max(1, selected.size - 1))
        candidate_idx = np.argpartition(-sim, kth=k - 1, axis=1)[:, :k]
        same = y[candidate_idx] == y[:, None]
        candidate_valid = valid[candidate_idx] & valid[:, None]
        for group, mask in masks.items():
            if not mask.any():
                same_count = 0
                total = 0
            else:
                group_valid = candidate_valid & mask[:, None]
                same_count = int((same & group_valid).sum())
                total = int(group_valid.sum())
            rate = same_count / total if total else math.nan
            rows.append(
                {
                    "diagnostic_type": "hard_negative",
                    "group": group,
                    "batch_size": "",
                    "top_k": k,
                    "total_negative_pairs": total,
                    "same_class_negative_pairs": same_count,
                    "false_negative_rate": "",
                    "hard_negative_same_class_rate": rate,
                    "hard_negative_cross_class_rate": 1 - rate if total else math.nan,
                    "hard_negative_false_negative_rate": rate,
                    "anchors_evaluated": int(mask.sum()),
                    "embedding_source": embedding_source,
                    "labels_posthoc_only": True,
                }
            )
    return rows


def write_csv_rows(path: str, fieldnames: Sequence[str], rows: Iterable[Dict[str, object]], append: bool = True) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = list(rows)
    file_exists = output.exists() and append
    with output.open("a" if append else "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        if not file_exists:
            writer.writeheader()
        for row in rows:
            writer.writerow({field: _format_value(row.get(field, "")) for field in fieldnames})


def read_csv_rows(path: str) -> List[Dict[str, str]]:
    p = Path(path)
    if not p.exists():
        return []
    with p.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _format_value(value: object) -> object:
    if isinstance(value, float):
        if math.isnan(value):
            return "NaN"
        return f"{value:.8g}"
    if isinstance(value, (np.floating,)):
        number = float(value)
        if math.isnan(number):
            return "NaN"
        return f"{number:.8g}"
    if isinstance(value, (np.integer,)):
        return int(value)
    return value


def numeric(value: object, default: float = math.nan) -> float:
    try:
        if value in {"", None, "NaN"}:
            return default
        return float(value)
    except Exception:
        return default

