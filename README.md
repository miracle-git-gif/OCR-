Mineru 本地部署指南 (macOS + Anaconda)
环境准备

1. 安装 Anaconda

bash
# 下载 Anaconda 

2. 配置 Conda 环境

将 Anaconda 添加到 PATH（如果尚未配置）：

1. 激活 Mineru 环境

bash
# 激活 mineru 环境
conda activate mineru

# 如果环境不存在，可能需要先创建
# conda create -n mineru python=3.10
# conda activate mineru
2. 运行 Mineru

使用以下命令运行：

bash
mineru -p /Users/dream/Desktop/merged_output_Redacted.pdf -o ./test -d cpu

3. 完整部署流程
conda activate mineru
mineru -p /Users/dream/Desktop/merged_output_Redacted.pdf -o ./test -d cpu

完成部署后，查看layout PDF，发现有一些表格被识别成图片。
重新添加了mineru.json配置文件
使用req.py完成对图片进行二次解析
