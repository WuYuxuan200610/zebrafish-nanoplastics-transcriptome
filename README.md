# Zebrafish Nanoplastics Transcriptome

## 斑马鱼中的纳米塑料转录组

基于斑马鱼 PS-NPs 暴露 RNA-seq count matrix 的探索性转录组分析项目。

> 注：本项目每组只有 1 个样本，没有生物学重复。因此当前结果属于基于 fold-change 阈值的探索性候选基因筛选，并未进行 DESeq2/edgeR 统计建模，也没有 p-value 和 FDR。请不要将“candidate genes”表述为统计显著的 DEGs。

## 项目背景

本项目分析斑马鱼在不同浓度聚苯乙烯纳米塑料（PS-NPs）暴露下的基因表达变化，探索微塑料暴露相关的候选差异基因、剂量响应和潜在生物学通路。

## 样本设计

|样本|处理|浓度|
|-|-|-|
|`wt`|对照|无|
|`low`|0.1 mg/L PS-NPs|0.1 毫克/升聚苯乙烯纳米粒子|
|`High`|10 mg/L PS-NPs|10 毫克/升聚苯乙烯纳米粒子|

注意：当前数据为 3 个样本、每组 1 个生物学重复。

## 主要结果

* 原始矩阵：32,520 个基因
* 低表达过滤后：22,298 个基因
* High vs WT 候选基因：372 个
* low vs WT 候选基因：447 个
* 浓度依赖性候选上调基因：363 个
* 浓度依赖性候选下调基因：32 个

主要图表位于 `results/figures/`，候选基因和富集分析输入位于 `results/tables/`。

## 用本仓库中代码所画出的图示意
## Results

### Sample QC

![Sample correlation](results/figures/fig01_sample_correlation.png)

![Expression distribution](results/figures/fig02_expression_distribution.png)

![PCA](results/figures/fig03_pca.png)

![Sample distance](results/figures/fig04_sample_distance.png)

### Candidate gene analysis

![Fold-change distribution](results/figures/fig05_fold_change_distribution.png)

![MA plots](results/figures/fig06_ma_plots.png)

![Top 50 clustered heatmap](results/figures/fig07_top50_clustered_heatmap.png)

### Dose response

![Dose response](results/figures/fig08_dose_response.png)

## 可供参考

富集结果图及更加具体的图片结果分析推荐查看项目报告，其中也有更详细的背景阐述和技术描述。报告中图片类型与此处展示图片类型一致，但细节、配色稍有不同。

[查看或下载完整实验报告](docs/report.pdf)  相信你看完报告后能对这个仓库有更好的理解（😄）

## 复现方法

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts

ctivate
pip install -r requirements.txt
python run\_all.py
```

## 分析方法

1. 原始 count matrix 检查
2. 低表达基因过滤
3. `log2(count + 1)` 转换
4. High vs WT、low vs WT fold-change 计算
5. 基于 `|log2FC| > 1` 和表达量阈值筛选候选基因
6. 样本 QC、PCA、MA 图、聚类热图和剂量响应可视化
7. 整理候选基因列表，用于 Metascape 网页版 GO/PPI 富集分析

完整方法说明见：`docs/analysis\_notes.md`。

## 项目局限性

* 每组只有 1 个样本，无法估计生物学重复内变异。
* 当前结果没有 p-value 或 FDR。
* 未进行 DESeq2、edgeR 或 limma-voom 差异表达建模。
* 结果应解释为探索性候选基因和生物学线索。

## 目录结构

```text
zebrafish-nanoplastics-transcriptome/
├── data/
├── docs/
├── results/
├── scripts/
├── run\_all.py
├── requirements.txt
├── README.md
├── LICENSE
└── UPLOAD\_WITH\_GITHUB\_DESKTOP.md
```

本仓库是公开展示的精简版：不包含原始个人课程报告，也不包含完整 Metascape 工作簿；仅保留 Top enrichment summary。

所有分析部分代码为本人借助AI辅助完成，实验前置的斑马鱼心脏解剖、送测为小组四人共同完成。

