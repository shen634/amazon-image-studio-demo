# Amazon Image Studio (local demo)

最小可运行 demo：本地去背景、居中白底、生成 JPEG 主图并输出 QA 报告。完全离线处理，不调用外部 API。

快速运行（Linux / macOS / Windows WSL）
1. git clone https://github.com/shen634/amazon-image-studio-demo && cd amazon-image-studio-demo
2. python -m venv venv
3. source venv/bin/activate   (Windows: venv\Scripts\activate)
4. pip install -r requirements.txt
5. python app.py
6. 在另一个终端：cd mcp/widget && python -m http.server 8000
7. 浏览器打开 http://localhost:8000/index.html ，选择图片点击“处理并生成主图”
8. 输出文件保存在 data/out/；报告为 CSV

注意
- rembg 需要额外模型文件，会在首次运行时下载/缓存；某些系统需要额外的系统依赖（libglib 等）。
- 如果你要把 widget 当作 Codex 的 MCP widget 使用，需要把 mcp/ 打包为 MCP bundle 并把后端部署在宿主可访问的地址（或使用隧道）。
- 我可以把这个 demo 推到你的 GitHub，或打包成 MCP 项目，或在 demo 上加入 QA/批量/HTML 审核页面。
