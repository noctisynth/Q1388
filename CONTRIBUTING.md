# 贡献指南

## 约定式提交

我们遵循约定式提交规范来编写我们的提交消息。每个提交消息应该具有以下格式：

```plain-text
<类型>(<范围>): <描述>

[可选正文]

[可选页脚]
```

其中 `<类型>` 应该是以下之一：

- **feat**: 新功能
- **fix**: 修复 Bug
- **docs**: 文档更改
- **style**: 不影响代码含义的更改（如空格、格式化、缺失的分号等）
- **refactor**: 代码重构
- **test**: 添加缺失的测试或更正现有测试
- **chore**: 对构建过程或辅助工具和库的更改（如文档生成）

## 贡献

### 技术栈

- 前端使用 `Vue.js`
- 后端使用 `Django`

### 依赖项

1. 依赖项配置

   - 前端：

   ```bash
   pnpm install
   ```

   - 后端：

   ```bash
   pdm install
   ```

2. 为更改创建一个新的分支：

   ```bash
   git checkout -b new-feature
   ```

3. 进行更改并按照约定式提交规范进行提交。
4. 将更改推送到 Fork 的仓库：

   ```bash
   git push origin new-feature
   ```

5. 向主仓库的 `main` 分支提交拉取请求。

### 环境更改

1. 前端

   ```bash
   pnpm add new-package
   ```

2. 后端

   ```bash
   pdm add new-package
   ```

## 代码风格

请注意进行 Code Lint 确保代码符合相关标准（如`PEP8`或`Black`）。
