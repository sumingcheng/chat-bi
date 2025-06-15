# GitHub Actions 自动构建部署说明

## 🚀 功能介绍

这个 GitHub Actions 工作流会在你推送 tag（以 `v` 开头）时自动构建和推送 Docker 镜像到 GitHub Container Registry。

## 📋 工作流特性

- ✅ 只在推送 tag 时触发（如：`v1.0.0`、`v2.1.0`）
- ✅ 自动构建前端和后端 Docker 镜像
- ✅ 支持多架构构建（linux/amd64、linux/arm64）
- ✅ 使用 GitHub Container Registry 存储镜像
- ✅ 支持 Docker 缓存优化构建速度
- ✅ 自动生成语义化版本标签
- ✅ 构建完成后生成部署摘要

## 🔧 如何使用

### 1. 推送代码并创建 tag

```bash
# 提交你的代码
git add .
git commit -m "feat: 添加新功能"
git push origin main

# 创建并推送 tag
git tag v1.0.0
git push origin v1.0.0
```

### 2. 查看构建状态

推送 tag 后，访问你的 GitHub 仓库的 "Actions" 标签页，可以看到自动触发的构建任务。

### 3. 使用构建的镜像

构建完成后，你可以使用以下命令拉取镜像：

```bash
# 拉取后端镜像
docker pull ghcr.io/你的用户名/chat-bi-api:v1.0.0

# 拉取前端镜像
docker pull ghcr.io/你的用户名/chat-bi-frontend:v1.0.0
```

## 🏷️ 标签说明

工作流会自动为每个镜像生成以下标签：

- `v1.0.0` - 具体版本号
- `v1.0` - 主版本号.次版本号
- `latest` - 最新版本

## 🔐 权限说明

这个工作流使用 `GITHUB_TOKEN` 自动认证，无需额外配置。GitHub 会自动为 Actions 提供必要的权限来推送到 GitHub Container Registry。

## 📦 镜像存储位置

- 后端镜像：`ghcr.io/你的用户名/chat-bi-api`
- 前端镜像：`ghcr.io/你的用户名/chat-bi-frontend`

## 🔄 可选配置

### 同时推送到 Docker Hub

如果你想同时推送到 Docker Hub，可以：

1. 在仓库的 Settings → Secrets and variables → Actions 中添加：
   - `DOCKERHUB_USERNAME`: 你的 Docker Hub 用户名
   - `DOCKERHUB_TOKEN`: 你的 Docker Hub 访问令牌

2. 取消工作流文件中 Docker Hub 登录步骤的注释

### 修改镜像名称

在工作流文件的 `env` 部分修改：

```yaml
env:
  REGISTRY: ghcr.io
  BACKEND_IMAGE_NAME: 你的后端镜像名
  FRONTEND_IMAGE_NAME: 你的前端镜像名
```

## 🛠️ 故障排除

### 构建失败常见原因

1. **Docker 文件路径错误**: 确保 Dockerfile 路径正确
2. **依赖安装失败**: 检查 package.json 或 requirements.txt
3. **权限问题**: 确保仓库有访问 GitHub Container Registry 的权限

### 查看构建日志

在 GitHub 仓库的 Actions 页面点击具体的构建任务，可以查看详细的构建日志。 