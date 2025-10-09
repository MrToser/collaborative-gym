import docker, requests, time
import socket
client = docker.from_env()

# 取外层容器所在的网络
outer = client.containers.get(socket.gethostname())
outer_net = list(outer.attrs["NetworkSettings"]["Networks"].keys())[0]
print(f"外层容器网络: {outer_net}")

# 启动内层容器加入同一网络
container = client.containers.run(
    "cogym-jupyter-cpu-image",
    # entrypoint="",
    detach=True,
    network=outer_net,  # 加入外层容器所在网络
    environment={"TOKEN": ""},
    
)

time.sleep(3)
container.reload()
inner_ip = container.attrs["NetworkSettings"]["Networks"][outer_net]["IPAddress"]
print(f"内层容器 IP: {inner_ip}")

# 直接用 IP 访问
try:
    r = requests.get(f"http://{inner_ip}:8888/api/kernels", timeout=10)
    print(f"✅ 成功访问! status={r.status_code}")
    print(r.text[:200])
except Exception as e:
    print("❌ 访问失败:", e)

container.remove(force=True)
