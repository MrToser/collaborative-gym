#!/bin/bash
set -e

# ==== 基础配置 ====
IMAGE_NAME="cogym-jupyter-cpu-image"
CONTAINER_NAME="cogym-jupyter-test"
PORT=8888

# ==== 确认挂载路径 ====
# 宿主机视角路径（根据 AutoDL 的映射结构）
HOST_PATH="/data_nvme/privatecloud/data/autodl-container-6c4642a0d1-f7a79d5c-storage/collaborative-gym/tmp/env_tabular_analysis_0"

# 容器内挂载目标路径
CONTAINER_PATH="/home/jovyan/work"

# ==== 创建测试用目录（防止路径不存在）====
mkdir -p "${HOST_PATH}"

# ==== 删除旧容器 ====
docker rm -f "${CONTAINER_NAME}" 2>/dev/null || true

# ==== 启动容器 ====
docker run -d \
  --name "${CONTAINER_NAME}" \
  -p ${PORT}:8888 \
  -v "${HOST_PATH}:${CONTAINER_PATH}:rw" \
  "${IMAGE_NAME}"

# ==== 打印提示 ====
echo "✅ 容器 ${CONTAINER_NAME} 已启动"
echo "挂载：${HOST_PATH} → ${CONTAINER_PATH}"
echo "访问 Jupyter: http://localhost:${PORT}"
