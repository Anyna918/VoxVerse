# VoxVerse（回声宇宙）

VoxVerse：在声音的宇宙里，每个回声都讲述一个故事。探索无限可能，与过去和未来对话。

## 项目简介

VoxVerse 是一个语音创新平台，结合了先进的语音模拟技术和 AI 聊天功能，为用户提供了一种独特的交互体验。它允许用户上传语音样本，模拟特定的声音进行聊天，使用户能够听到熟悉的声音或体验新的声音。无论是虚拟导游、练习演讲、提供心理健康支持，还是简单的娱乐，VoxVerse 都能满足您的需求。

## 特性

- **声音模拟**：上传语音样本，模拟任意声音。
- **AI 聊天**：集成了文心一言接口，提供流畅的聊天体验。
- **多用途**：适用于教育、娱乐、心理支持等多种场景。
- **用户友好**：简洁的用户界面，易于操作。

## 运行环境

- 前端

  利用uni-app编写。自行运行时需要注册HBuilderX账号，进而调用其中的云函数

- 后端

  后端主要通过flask框架进行编写

  - **依赖库**：Flask, Librosa, torch等（具体请见 `requirements.txt`）

  当在本地运行时，需要将前端请求接口的地址更改为本地局域网下计算机的ip地址。例如，在Windows环境下，利用`ipconfig`在命令行中查看ip地址

## 安装指南

1. 克隆仓库：

   ```
   git clone https://github.com/yourusername/voxverse.git
   ```

2. 进入项目目录：

   ```
   cd voxverse
   ```

3. 安装依赖：

   ```
   // 选择运行的python环境，进行依赖安装
   pip install -r requirements.txt
   ```

## AI模拟模型

这里主要运用了`MockingBird`模型进行语音合成，参考链接如下：

[MockingBird: 🚀AI拟声: 5秒内克隆您的声音并生成任意语音内容](https://github.com/babysor/MockingBird)

### 预训练模型：阿里云盘https://www.alipan.com/s/sSdgLa2xihg

## 贡献

我们欢迎所有形式的贡献，无论是新功能、文档改进，还是问题报告，均欢迎大家进行交流
