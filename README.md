# GCL Literature Review

本项目用于系统整理 Graph Contrastive Learning, GCL、图自监督学习、图增强、负样本处理、GraphMAE 类生成式图自监督、异配图学习、大规模图对比学习、图基础模型等方向的论文，为偏方法型顶会/顶刊论文选题、方法设计和实验对照提供可追溯的文献证据。

## 项目目标

- 建立统一的论文阅读表，记录每篇论文的方法问题、核心思想、实验设置、贡献声明、弱点与潜在 gap。
- 将论文事实与阅读者推断分开记录，避免把未确认信息写成确定结论。
- 为后续方法分类、baseline 选择、实验设计和论文写作积累证据。

## 文件结构

```text
gcl-literature-review/
├── papers/
│   ├── pdf/                  # 存放论文 PDF
│   ├── bib/                  # 存放 BibTeX 或引用信息
│   └── notes/                # 存放逐篇论文阅读笔记
├── scripts/                  # 后续自动化脚本
├── outputs/
│   ├── seed_papers.csv       # 种子论文表
│   ├── seed_papers.md        # 种子论文说明与人工清单
│   ├── gcl_literature_table.csv
│   ├── gcl_literature_table.xlsx
│   ├── method_taxonomy.md    # 方法分类沉淀
│   └── candidate_gaps.md     # 候选研究空白
├── prompts/
│   └── extraction_prompt.md  # 逐篇论文信息抽取提示词
└── README.md
```

## 使用方法

1. 将已确认的论文 PDF 放入 `papers/pdf/`，BibTeX 放入 `papers/bib/`。
2. 对每篇论文使用 `prompts/extraction_prompt.md` 抽取结构化信息。
3. 将抽取结果写入 `outputs/gcl_literature_table.csv` 或 `outputs/gcl_literature_table.xlsx`。
4. 对无法从论文中确认的字段，统一填写 `Unknown`。
5. `Evidence` 字段必须记录证据来源，例如 `Abstract`、`Section 3`、`Table 2`、`Appendix` 等。
6. 阅读到一定数量后，再更新 `outputs/method_taxonomy.md` 和 `outputs/candidate_gaps.md`，形成方法谱系与可验证 gap。

## 文献表字段

文献主表包含以下字段：

```text
Paper, Year, Venue, Task, Graph Type, Method Category, Core Problem, Main Idea, Encoder, View Generation, Positive Pair Definition, Negative Sampling, Objective, Claimed Contribution, Theoretical Analysis, Datasets, Baselines, Strongest Baseline, Metrics, Ablation, Complexity, Code Available, Weakness, Missing Experiments, Hidden Assumption, Possible Gap, Relevance Score, Evidence
```

## 质量约束

- 不编造论文信息。
- 论文标题、方法名、数据集名、会议名可以保留英文。
- 若字段无法确认，填写 `Unknown`。
- `Evidence` 必须能帮助回到原文位置复核。
- `Weakness`、`Missing Experiments`、`Hidden Assumption`、`Possible Gap` 可包含阅读者判断，但必须写清证据来源或推断依据。
