# 分析说明

## 1\. 项目定位

本项目是**探索性 fold-change 分析**，不是完整的统计差异表达分析。

原因是当前样本设计为：

* WT：1 个样本
* low：1 个样本
* High：1 个样本

没有生物学重复意味着无法可靠估计组内方差，也无法计算严格意义上的 p-value 和 FDR。

## 2\. 数据预处理

原始文件：`data/raw/gene\_expression\_matrix.csv`

处理步骤：

1. 将第一列统一命名为 `GeneID` 并设置为索引。
2. 检查重复 GeneID；若存在则按 GeneID 求和。
3. 过滤低表达基因：至少在 2 个样本中 `count > 10`。
4. 对保留基因保存清洗后的 count matrix。

过滤结果：

* 原始基因数：32,520
* 保留基因数：22,298

## 3\. Fold-change 计算

使用 `log2(count + 1)` 计算：

```text
High\_log2FC = log2(High + 1) - log2(wt + 1)
low\_log2FC  = log2(low + 1) - log2(wt + 1)
```

候选基因筛选规则：

```text
|log2FC| > 1
且 max(raw expression in comparison pair) > 50
```

这里的“候选基因”是基于阈值的探索性筛选结果。

## 4\. 不标准火山图

标准火山图通常使用：

* x 轴：log2 fold-change
* y 轴：`-log10(p-value)` 或 `-log10(adjusted p-value)`

当前项目没有统计 p-value，因此仓库命名为：

```text
fig05\_fold\_change\_distribution.png
```

并将 y 轴明确标为：

```text
Fold-change magnitude: -log10(|log2FC| + 0.01)
```

## 5\. 样本 QC 解读

本项目生成以下样本级图形：

* 样本相关性热图
* 表达分布箱线图
* PCA
* 样本距离热图

这些图可用于观察样本间整体关系，但由于每组只有 1 个样本，不能用来证明组间差异显著。

## 6\. 热图说明

热图展示按 fold-change 排序得到的 Top 50 基因：

* 行：基因
* 列：样本
* 值：按基因行进行 Z-score 标准化后的 `log2(count + 1)`
* 行和列均进行层次聚类

## 7\. 剂量响应说明

“浓度依赖性候选上调/下调”定义为：

* low vs WT 的 log2FC 与 High vs WT 的 log2FC 均 `> 1`，或
* 二者均 `< -1`

这只能说明两个浓度下方向一致，不等同于严格单调剂量反应，也不能提供显著性证据。

## 8\. 富集分析说明

GO/PPI 富集分析通过Metascape 网页平台完成。仓库中的 Python 脚本负责生成 Metascape 输入基因列表并整理候选基因；实际的富集计算、PPI 网络和网页图形由 Metascape 生成。

本精简仓库保留 `results/tables/metascape\_top\_enrichments.csv` 作为结果摘要。

仓库生成 6 个候选基因列表：

* `high\_vs\_wt\_up.txt`
* `high\_vs\_wt\_down.txt`
* `low\_vs\_wt\_up.txt`
* `low\_vs\_wt\_down.txt`
* `concentration\_dependent\_up.txt`
* `concentration\_dependent\_down.txt`

Metascape 原始输出保存在 `external\_results/metascape/`。

