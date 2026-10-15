# GitHub Desktop 上传步骤

这份文件夹已经按 GitHub 项目整理好了。推荐用 GitHub Desktop 上传，基本不需要输入 Git 命令。

## 1. 安装 GitHub Desktop

下载地址：

```text
https://desktop.github.com/
```

安装后登录你的 GitHub 账号。

## 2. 解压这个压缩包

解压后得到：

```text
zebrafish-nanoplastics-transcriptome-upload/
```

## 3. 用 GitHub Desktop 打开文件夹

打开 GitHub Desktop，选择：

```text
File → Add local repository
```

点击 `Choose`，选中解压后的 `zebrafish-nanoplastics-transcriptome-upload` 文件夹，然后点击 `Add repository`。

## 4. 创建首次提交

左侧会显示项目文件。

在 `Summary` 中填写：

```text
Initial exploratory transcriptome analysis project
```

然后点击：

```text
Commit to main
```

## 5. 发布到 GitHub

点击顶部：

```text
Publish repository
```

填写：

### Name

```text
zebrafish-nanoplastics-transcriptome
```

### Description

```text
Exploratory transcriptomic analysis of zebrafish exposed to polystyrene nanoplastics
```

如果你准备公开，取消 `Keep this code private`；如果还没确认是否公开，就保持私有。

最后点击：

```text
Publish repository
```

## 6. 检查上传结果

上传成功后，点击 GitHub Desktop 中的：

```text
View on GitHub
```

确认页面中能看到 `README.md`、`scripts/`、`results/` 和 `data/`。

## 注意事项

- 这个精简版已经去掉了原始个人课程报告。
- 原始 count matrix 已保留，因此别人可以复现主要分析。
- 如果你想完全公开仓库，仍建议先确认实验数据是否允许公开。
