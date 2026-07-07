# Baseline Collision Check

## ProGCL / GDCL / IFL-GCL 解决了什么

这些方法主要攻击 negative side。

- ProGCL 关注 hard negative / false negative 的概率建模和对比损失修正。
- GDCL 关注 false negative 或 noisy negative 对 GCL 的影响。
- IFL-GCL 从 Positive-Unlabeled 视角解释 GCL，并挖掘 non-augmented positives。

它们对 Gap 2 的压力是：如果本项目只做 negative reweighting，很容易被认为已经被覆盖。

## ROSEN 解决了什么

ROSEN 明确指出 heterophily local positive sampling 会产生 false positive samples，并通过局部同配结构重构缓解这个问题。它对 Gap 2 的压力是：如果本项目只说“异配图 positive view 有噪声”，新颖性不足。

## HLCL / PolyGCL / HeterGCL / M3P-GCL 解决了什么

- HLCL 通过 low-pass / high-pass graph filters 构造 heterophily-aware contrastive views。
- PolyGCL 用 learnable spectral polynomial filters 引入 high-pass / low-pass 信息。
- HeterGCL 放弃普通随机增强，结合结构和语义学习处理异配图。
- M3P-GCL 用 structural / attribute views 与 macro-micro message passing 改善异配场景。

它们对 Gap 2 的压力是：普通 heterophily-aware augmentation 不再能作为主 claim。剩余空间必须落在可诊断、可校准的 positive-negative pair reliability。

## HGMS 解决了什么

HGMS 面向 heterogeneous graph / metapath 场景，用 connection-strength-guided heterogeneous edge dropping 和 multi-view self-expression 缓解异构图中的同配增强与 false negative 问题。

它对 Gap 2 的压力是：如果本项目要声称跨图类型，需要解释为什么 homogeneous heterophily、heterogeneous graph 和 TAG 场景共享同一个 reliability 问题，而不是只套用 HGMS 的连接强度思想。

## GAugLLM / GCL-OT 对 Gap 7 的影响

GAugLLM 已经覆盖普通 LLM augmentation，GCL-OT 已经推进 heterophilic text-attributed graph alignment。因此 Gap 7 不能再以普通 LLM/TAG augmentation 作为主 claim，只能聚焦 structure-text conflict、cross-modal pair reliability 和 conflict-aware diagnostics。

## 为什么 Gap 2 仍然可能成立

Gap 2 的剩余空间不在“发现 false negative”或“发现异配图 view 噪声”，而在以下组合：

1. 在同一 protocol 下同时测 positive view failure 与 negative pair collision。
2. 证明二者在低同配节点、强增强或 hard-negative mining 下可能共现。
3. 区分 true-hard、false-hard、uncertain-hard，而不是简单降低所有 hard negatives。
4. 给出 pair-level reliability diagnostics，解释现有 heterophily-aware view construction 为什么仍缺少校准信号。

## Gap 2 的最小新颖性边界

最小边界应是：

- 不只修正 negative，也不只修正 positive。
- 不把标签用于训练，只在实验后验证 reliability 行为。
- 不把普通 heterophily-aware augmentation 或普通 LLM/TAG augmentation 作为贡献。
- 至少证明一个稳定 failure pattern：低同配 / 异配图上 positive failure 与 hard-negative false negative 同时上升。
- 方法设计阶段必须围绕统一 reliability variable，而不是简单换 augmentation 或换 loss。

