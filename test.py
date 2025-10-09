import docker, socket, requests

client = docker.from_env()

# 1️⃣ 启动一个简单HTTP服务的容器（比如 python -m http.server）
container = client.containers.run(
    "cogym-jupyter-cpu-image",
    command=["bash", "-lc", "python -m http.server 8888"],
    entrypoint="", 
    detach=True,
    publish_all_ports=True,  # 自动发布 EXPOSE 或默认端口
)

container.reload()
print("Container ports:", container.ports)

# 获取宿主机随机映射的端口
host_port = container.ports['8888/tcp'][0]['HostPort']
print("HostPort assigned:", host_port)

# 2️⃣ 尝试从外层容器内部访问 localhost:<host_port>
print("\nTrying to access from current (outer) container ...")
try:
    r = requests.get(f"http://127.0.0.1:{host_port}", timeout=2)
    print(f"✅ Outer container can reach it! status={r.status_code}")
except Exception as e:
    print(f"❌ Outer container cannot reach localhost:{host_port}")
    print("   (This means it's not bound inside this container.)")

# 3️⃣ 探测 Docker 网关 (宿主机在容器视角的地址)
print("\nFinding default gateway ...")
gw_ip = None
with open("/proc/net/route") as f:
    for line in f:
        parts = line.split()
        if parts[1] != '00000000' or not int(parts[3], 16) & 2:
            continue
        gw_ip = socket.inet_ntoa(bytes.fromhex(parts[2])[::-1])
        break

if gw_ip:
    print("Gateway (likely host) IP:", gw_ip)
    try:
        r = requests.get(f"http://{gw_ip}:{host_port}", timeout=2)
        print(f"✅ Gateway access works! status={r.status_code}")
    except Exception:
        print(f"❌ Gateway access also failed.")
else:
    print("Could not detect default gateway IP.")

print("\nContainer logs:")
print(container.logs().decode())
print("Container status:")
print(container.status)

# 4️⃣ 清理容器
container.remove(force=True)
