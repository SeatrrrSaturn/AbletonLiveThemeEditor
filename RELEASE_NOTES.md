## LiveThemeEditor v1.1.0

Ableton Live 12 主题配色编辑器 —— 图形界面改 `.ask` 主题，右侧仿 Live 实时预览。

### 本版新增
- **随机配色**：一键换一套。
  - *整体随机* —— 全主题统一一个随机色相 + 随机饱和/亮度系数，明暗层次和灰色骨架保留，改完基本能直接看。
  - *逐色随机* —— 每个色值各拿一个随机色相，最花，适合找灵感。
  - 两种都跳过灰色（背景/文字/层级不变），各算一步撤销，可以连点到满意为止。
- 附带三个示例主题：`examples/Wine Dark.ask`、`Forest Light.ask`、`Mono Grey.ask`
- README 增加改前/改后对比图与六个预设的轮播 GIF

### 下载
- `LiveThemeEditor-v1.1.0-win64.zip` — 解压即用，不需要装 Python（Windows 10/11 64 位）；压缩包内含 exe、README、LICENSE 和三个示例主题

### 功能
- 276 个色值按语义分组，中英双语名，中英文都能搜
- 点色块调系统取色器，或直接改十六进制（支持 `#RRGGBBAA`）
- 配色方案：色相偏移 / 饱和度 / 亮度整体调色 + 6 个预设，整批可撤销
- 保存只替换对应行，不动 XML 结构；改 N 个色值就只有 N 行变化
- 一键安装到 `Resources/Themes`，重启 Live 后在 设置 → Look and Feel → Theme 里选
- 自动探测主题目录，也可手动指定

### 说明
- exe 未签名，首次运行可能弹 SmartScreen，选「更多信息 → 仍要运行」
- 建议先「另存为」自定义名字再安装，别直接覆盖 Live 自带的 `Default *.ask`

### 校验
`SHA256(zip): 23146a262150ce5cbe6251ce342c5272a08603cd7f771e260402c3c4bfc56010`
`SHA256(exe): 73a42473c8ee39aa62c5f233c4d79597be9fdefefedb2dd807672b28ee7331d9`
