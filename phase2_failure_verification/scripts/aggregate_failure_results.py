from __future__ import annotations

import argparse
import math
from collections import defaultdict
from pathlib import Path

from utils import numeric, read_csv_rows, setup_logger, write_csv_rows


JOINT_FIELDNAMES = [
    "dataset",
    "augmentation_type",
    "augmentation_rate",
    "local_homophily_group",
    "positive_failure_score",
    "negative_collision_score",
    "joint_reliability_risk_score",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aggregate Phase 2 failure verification outputs.")
    parser.add_argument(
        "--graph-statistics",
        default="phase2_failure_verification/outputs/tables/graph_statistics.csv",
    )
    parser.add_argument(
        "--positive-view-failure",
        default="phase2_failure_verification/outputs/tables/positive_view_failure.csv",
    )
    parser.add_argument(
        "--negative-pair-noise",
        default="phase2_failure_verification/outputs/tables/negative_pair_noise.csv",
    )
    parser.add_argument(
        "--joint-output",
        default="phase2_failure_verification/outputs/tables/joint_reliability_risk.csv",
    )
    parser.add_argument(
        "--report-output",
        default="phase2_failure_verification/outputs/reports/failure_verification_summary.md",
    )
    parser.add_argument("--log-path", default=None)
    return parser.parse_args()


def _mean(values):
    values = [v for v in values if math.isfinite(v)]
    return sum(values) / len(values) if values else math.nan


def _normalize_by_max(items):
    finite = [value for value in items if math.isfinite(value)]
    if not finite:
        return [math.nan for _ in items]
    max_value = max(finite)
    if max_value <= 0:
        return [0.0 if math.isfinite(value) else math.nan for value in items]
    return [value / max_value if math.isfinite(value) else math.nan for value in items]


def build_joint_rows(positive_rows, negative_rows):
    positive_scores = defaultdict(list)
    for row in positive_rows:
        score = _mean(
            [
                numeric(row.get("neighbor_label_distribution_js_divergence")),
                abs(numeric(row.get("local_homophily_change"))),
                numeric(row.get("low_reliability_positive_ratio")),
            ]
        )
        key = (
            row.get("dataset", ""),
            row.get("augmentation_type", ""),
            row.get("augmentation_rate", ""),
            row.get("local_homophily_group", "all"),
        )
        positive_scores[key].append(score)

    negative_scores = defaultdict(list)
    for row in negative_rows:
        group = row.get("group", "all")
        if group not in {"all", "low_homophily", "medium_homophily", "high_homophily"}:
            continue
        score = _mean(
            [
                numeric(row.get("false_negative_rate")),
                numeric(row.get("hard_negative_false_negative_rate")),
            ]
        )
        key = (row.get("dataset", ""), group)
        negative_scores[key].append(score)

    raw_rows = []
    for key, values in positive_scores.items():
        dataset, augmentation_type, augmentation_rate, group = key
        raw_rows.append(
            {
                "dataset": dataset,
                "augmentation_type": augmentation_type,
                "augmentation_rate": augmentation_rate,
                "local_homophily_group": group,
                "positive_failure_score": _mean(values),
                "negative_collision_score": _mean(negative_scores.get((dataset, group), [])),
            }
        )

    pos_norm = _normalize_by_max([row["positive_failure_score"] for row in raw_rows])
    neg_norm = _normalize_by_max([row["negative_collision_score"] for row in raw_rows])
    for row, p, n in zip(raw_rows, pos_norm, neg_norm):
        if math.isfinite(p) and math.isfinite(n):
            row["joint_reliability_risk_score"] = p + n
        elif math.isfinite(p):
            row["joint_reliability_risk_score"] = p
        elif math.isfinite(n):
            row["joint_reliability_risk_score"] = n
        else:
            row["joint_reliability_risk_score"] = math.nan
    return raw_rows


def write_report(path: str, graph_rows, positive_rows, negative_rows, joint_rows) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    datasets = sorted({row.get("dataset", "") for row in graph_rows + positive_rows + negative_rows if row.get("dataset")})
    missing = []
    if not graph_rows:
        missing.append("graph_statistics.csv")
    if not positive_rows:
        missing.append("positive_view_failure.csv")
    if not negative_rows:
        missing.append("negative_pair_noise.csv")
    lines = [
        "# Failure Verification Summary",
        "",
        "## 当前状态",
        "",
        f"- 覆盖数据集：{', '.join(datasets) if datasets else '尚无结果'}",
        f"- graph statistics 行数：{len(graph_rows)}",
        f"- positive view failure 行数：{len(positive_rows)}",
        f"- negative pair noise 行数：{len(negative_rows)}",
        f"- joint reliability risk 行数：{len(joint_rows)}",
        f"- 缺失输入：{', '.join(missing) if missing else '无'}",
        "",
        "## 解释边界",
        "",
        "- 标签只用于后验 diagnostic analysis，不用于无监督训练、增强选择或目标优化。",
        "- raw feature / PCA / simple encoder 得到的 hard-negative 结果只能视为 proxy。",
        "- joint_reliability_risk_score 是第一版归一化加和，用于排序风险区域，不是论文主结论。",
        "",
        "## 初步判断规则",
        "",
        "- 若低同配或异配数据集同时出现更高 positive failure score 与 negative collision score，则 Gap 2 值得继续。",
        "- 若只出现 positive failure，应回到 Gap 1 的 view / positive reliability calibration。",
        "- 若只出现 batch/hard-negative collision，应转向 scalable mini-batch negative noise。",
        "- 若二者均不明显，不建议直接进入顶会方法主线。",
    ]
    if joint_rows:
        top = sorted(
            joint_rows,
            key=lambda row: numeric(row.get("joint_reliability_risk_score")),
            reverse=True,
        )[:10]
        lines.extend(["", "## Joint Risk Top Rows", "", "| Dataset | Augmentation | Rate | Group | Joint Risk |", "|---|---|---:|---|---:|"])
        for row in top:
            lines.append(
                f"| {row.get('dataset')} | {row.get('augmentation_type')} | {row.get('augmentation_rate')} | "
                f"{row.get('local_homophily_group')} | {row.get('joint_reliability_risk_score')} |"
            )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    logger = setup_logger(log_path=args.log_path)
    graph_rows = read_csv_rows(args.graph_statistics)
    positive_rows = read_csv_rows(args.positive_view_failure)
    negative_rows = read_csv_rows(args.negative_pair_noise)
    joint_rows = build_joint_rows(positive_rows, negative_rows)
    write_csv_rows(args.joint_output, JOINT_FIELDNAMES, joint_rows, append=False)
    write_report(args.report_output, graph_rows, positive_rows, negative_rows, joint_rows)
    logger.info("Wrote joint CSV to %s", args.joint_output)
    logger.info("Wrote report to %s", args.report_output)


if __name__ == "__main__":
    main()

