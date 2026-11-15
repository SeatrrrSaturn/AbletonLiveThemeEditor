## LiveThemeEditor v1.0.0

Ableton Live 12 主题配色编辑器 —— 图形界面改 `.ask` 主题，右侧仿 Live 实时预览。

### 下载
- `LiveThemeEditor-v1.0.0-win64.zip` — 解压即用，不需要装 Python（Windows 10/11 64 位）

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
`SHA256: 6115ab0505a58e95e8dfdf13da86a9067caeb34eb67bafdae2a2ecd00e4aaea0`