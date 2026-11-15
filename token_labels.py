# -*- coding: utf-8 -*-
"""Ableton Live 12 主题色值的中文名对照。

.theme 里每个 <Token Value=… /> 只有英文标识符，看名字根本不知道在改哪一块，
这里给 234 个已知色值配中文名，界面上以「中文名 / English」双语显示。
"""

# 电平表分组的中文名
VU_GROUP_ZH = {
    "StandardVuMeter": "标准电平表",
    "OverloadVuMeter": "过载电平表",
    "DisabledVuMeter": "停用电平表",
    "HeadphonesVuMeter": "耳机电平表",
    "SendsOnlyVuMeter": "仅发送电平表",
    "BipolarGainReductionVuMeter": "双极增益衰减表",
    "OrangeVuMeter": "橙色电平表",
}

# 电平表分段的中文名
VU_SEGMENT_ZH = {
    "Minimum": "最小（最暗段）",
    "BelowZeroDecibel2": "零下 2（深绿段）",
    "BelowZeroDecibel1": "零下 1（绿段）",
    "ZeroDecibel": "零点（黄绿段）",
    "AboveZeroDecibel": "零上（黄段）",
    "Maximum": "最大（红段）",
    "OnlyMinimumToMaximum": "仅显示最小到最大",
}

TOKEN_ZH = {
    "AbletonColor": "品牌强调色",
    "Alert": "警示色",
    "ArrangementRulerMarkings": "排列视图·标尺刻度",
    "ArrangerGridTiles": "排列视图·网格底色",
    "AutomationColor": "自动化曲线色",
    "AutomationDisabled": "自动化（禁用）",
    "AutomationGrid": "自动化网格线",
    "AutomationLaneClipBodyLightness": "自动化轨道·片段主体明度",
    "AutomationLaneClipBodySaturation": "自动化轨道·片段主体饱和度",
    "AutomationLaneHeaderLightness": "自动化轨道·轨头明度",
    "AutomationLaneHeaderNameLightness": "自动化轨道·轨头名称明度",
    "AutomationLaneHeaderNameSaturation": "自动化轨道·轨头名称饱和度",
    "AutomationLaneHeaderSaturation": "自动化轨道·轨头饱和度",
    "AutomationMouseOver": "自动化（悬停）",
    "AutomationTransformToolFrame": "自动化变换工具·框线",
    "AutomationTransformToolFrameActive": "自动化变换工具·框线（激活）",
    "AutomationTransformToolHandle": "自动化变换工具·手柄",
    "AutomationTransformToolHandleActive": "自动化变换工具·手柄（激活）",
    "BackgroundClip": "片段底色",
    "BackgroundClipFrame": "片段边框",
    "BipolReset": "双极旋钮·回中点",
    "BipolarPotiTriangle": "双极旋钮·三角指示",
    "BrowserBar": "浏览器栏底色",
    "BrowserBarOverlayHintTextColor": "浏览器栏·提示文字",
    "BrowserDisabledItem": "浏览器·禁用项目",
    "BrowserSampleWaveform": "浏览器·采样波形",
    "BrowserTagBackground": "浏览器·标签底色",
    "CheckControlNotCheckedBlendFactor": "勾选框·未勾选混合系数",
    "ChosenAlert": "警示色（按下）",
    "ChosenAlternative": "备选控件色（按下）",
    "ChosenDefault": "默认控件色（按下）",
    "ChosenPlay": "播放键（按下）",
    "ChosenPreListen": "预听键（按下）",
    "ChosenRecord": "录音键（按下）",
    "ClipBlendFactor": "片段颜色混合系数",
    "ClipBorder": "片段边框线",
    "ClipBorderAlpha": "片段边框透明度",
    "ClipContrastColorAdjustment": "片段颜色对比度调整",
    "ClipSlotButton": "片段槽按钮",
    "ClipText": "片段上的文字",
    "ControlBackground": "控件底色",
    "ControlContrastFrame": "控件对比边框",
    "ControlContrastTransport": "走带控件对比色",
    "ControlDisabled": "控件（禁用）",
    "ControlFillHandle": "推子/滑块手柄",
    "ControlForeground": "控件前景色（主文字）",
    "ControlOffDisabledForeground": "控件·关+禁用 前景",
    "ControlOffForeground": "控件·关 前景",
    "ControlOnAlternativeForeground": "控件·开（备选）前景",
    "ControlOnDisabledForeground": "控件·开+禁用 前景",
    "ControlOnForeground": "控件·开 前景",
    "ControlSelectionFrame": "控件选中框",
    "ControlTextBack": "控件文字衬底",
    "DeactivatedClipHeader": "停用片段·标题栏",
    "DeactivatedClipHeaderForeground": "停用片段·标题文字",
    "DeactivatedPoti": "停用旋钮",
    "DeactivatedPotiNeedle": "停用旋钮指针",
    "DefaultBlendFactor": "默认混合系数",
    "Desktop": "最底层背景（桌面）",
    "DetailGridTiles": "细节视图·网格底色",
    "DetailViewBackground": "细节视图·底色",
    "DetailViewRulerMarkings": "细节视图·标尺刻度",
    "DimmedWaveformColor": "暗化波形（未选中）",
    "DisabledContextMenuIconAlpha": "右键菜单·禁用图标透明度",
    "DisplayBackground": "显示屏/深底区域",
    "DrumRackScroller1": "鼓架·滚动条 1",
    "DrumRackScroller2": "鼓架·滚动条 2",
    "ExpressionLaneHeaderHighlight": "表情通道·头部高亮",
    "FilledDrumRackPad": "鼓架垫（已占用）",
    "FreezeColor": "冻结轨道色",
    "GainReductionLineColor": "增益衰减线",
    "GridGuideline": "网格辅助线",
    "GridLabel": "网格标签文字",
    "GridLineBase": "网格线基色",
    "IconBlendFactor": "图标混合系数",
    "ImplicitArm": "隐式预备录音（armed）",
    "InaudibleTakeLightness": "不可听 Take·明度",
    "InaudibleTakeNameLightness": "不可听 Take·名称明度",
    "InaudibleTakeNameSaturation": "不可听 Take·名称饱和度",
    "InaudibleTakeSaturation": "不可听 Take·饱和度",
    "InputCurveColor": "输入曲线色（EQ/包络）",
    "InputCurveOutlineColor": "输入曲线描边",
    "KeyZoneBackground": "键区（采样器映射）底色",
    "KeyZoneCrossfadeRamp": "键区·交叉渐变斜面",
    "LearnKey": "MIDI 学习·按键",
    "LearnMacro": "宏学习标记",
    "LearnMidi": "MIDI 学习标记",
    "LinkedTrackHover": "关联轨道（悬停）",
    "LoopColor": "循环区间色",
    "MainViewFocusIndicator": "主视图焦点指示",
    "MeterBackground": "电平表底色",
    "MidiEditorBackgroundWhiteKeySeparator": "MIDI 编辑器·白键分隔线",
    "MidiEditorBlackKeyBackground": "MIDI 编辑器·黑键底色",
    "MidiNoteMaxVelocity": "MIDI 音符·最大力度",
    "MinVelocityNoteBlendFactor": "最小力度音符混合系数",
    "MixSurfaceAreaBlendFactor": "混音台面板混合系数",
    "Modulation": "调制色",
    "ModulationDisabled": "调制（禁用）",
    "ModulationMouseOver": "调制（悬停）",
    "MutedAuditionClip": "静音试听片段",
    "NonEditableAutomationAlpha": "不可编辑自动化透明度",
    "NoteBorderStandbyBlendFactor": "音符边框·待命混合系数",
    "NoteDisabledSelectedBlendFactor": "音符禁用选中混合系数",
    "NoteProbability": "音符概率色",
    "OffGridGuideline": "网格外辅助线",
    "OffGridLoopColor": "循环区外颜色",
    "Operator1": "Operator·波形色 1",
    "Operator2": "Operator·波形色 2",
    "Operator3": "Operator·波形色 3",
    "Operator4": "Operator·波形色 4",
    "OutputCurveColor": "输出曲线色",
    "OutputCurveOutlineColor": "输出曲线描边",
    "PianoBlackKey": "钢琴黑键",
    "PianoKeySeparator": "琴键分隔线",
    "PianoWhiteKey": "钢琴白键",
    "Poti": "旋钮主体",
    "PotiNeedle": "旋钮指针",
    "PreferencesTab": "偏好设置页签",
    "Progress": "进度条填充",
    "ProgressText": "进度条文字",
    "RangeDefault": "数值条·默认",
    "RangeDisabled": "数值条·禁用",
    "RangeDisabledOff": "数值条·禁用(关)",
    "RangeEditField": "数值输入框",
    "RangeEditField2": "数值输入框 2",
    "RangeEditField3": "数值输入框 3",
    "RetroDisplayBackground": "LCD 显示屏底色",
    "RetroDisplayBackgroundLine": "LCD 显示屏底线",
    "RetroDisplayBlendFactor": "LCD 显示屏混合系数",
    "RetroDisplayControlSelectionFrame": "LCD 显示屏·选中框",
    "RetroDisplayForeground": "LCD 显示屏文字",
    "RetroDisplayForeground2": "LCD 显示屏文字 2",
    "RetroDisplayForegroundDisabled": "LCD 显示屏禁用文字",
    "RetroDisplayGreen": "LCD 绿色元素",
    "RetroDisplayHandle1": "LCD 手柄 1",
    "RetroDisplayHandle2": "LCD 手柄 2",
    "RetroDisplayRed": "LCD 红色元素",
    "RetroDisplayScaleText": "LCD 刻度文字",
    "RetroDisplayTitle": "LCD 标题文字",
    "ScaleAwareness": "音阶提示色（MIDI 编辑器）",
    "SceneContrast": "场景号底色",
    "ScrollBarAlpha": "滚动条透明度",
    "ScrollBarBackgroundAlpha": "滚动条背景透明度",
    "ScrollBarOnHoverAlpha": "滚动条悬停透明度",
    "ScrollbarInnerHandle": "内嵌滚动条·手柄",
    "ScrollbarInnerHandleHover": "内嵌滚动条·手柄（悬停）",
    "ScrollbarInnerTrack": "内嵌滚动条·轨道",
    "ScrollbarInnerTrackHover": "内嵌滚动条·轨道（悬停）",
    "ScrollbarLCDHandle": "LCD 滚动条·手柄",
    "ScrollbarLCDHandleHover": "LCD 滚动条·手柄（悬停）",
    "ScrollbarLCDTrack": "LCD 滚动条·轨道",
    "ScrollbarLCDTrackHover": "LCD 滚动条·轨道（悬停）",
    "ScrollbarMixerShowOnScrollHandle": "混音台滚动条·手柄",
    "ScrollbarMixerShowOnScrollHandleHover": "混音台滚动条·手柄（悬停）",
    "SearchIndication": "搜索高亮",
    "SearchIndicationStandby": "搜索高亮（待命）",
    "SecondarySelectionForeground": "次级选中·文字",
    "SelectionBackground": "选中底色",
    "SelectionBackgroundContrast": "选中底色对比",
    "SelectionForeground": "选中文字",
    "SelectionFrame": "选中框线",
    "SelectorZoneBackground": "选择区（采样器）底色",
    "SelectorZoneCrossfadeRamp": "选择区·交叉渐变斜面",
    "SessionSlotOklabLCompensationFactor": "Session 槽位亮度补偿系数",
    "ShadowDark": "深阴影",
    "ShadowLight": "浅阴影",
    "SpectrumAlternativeColor": "频谱·备选色",
    "SpectrumDefaultColor": "频谱·默认色",
    "SpectrumGridLines": "频谱网格线",
    "StandbySelectionBackground": "待命选中·底色",
    "StandbySelectionForeground": "待命选中·文字",
    "StripedBackgroundShadeFactor": "条纹背景明暗系数",
    "SurfaceArea": "面板区域底色",
    "SurfaceAreaFocus": "面板区域·焦点",
    "SurfaceBackground": "表面底色",
    "SurfaceHighlight": "表面高亮",
    "TakeLaneHeaderLightness": "Take 通道·头部明度",
    "TakeLaneHeaderNameLightness": "Take 通道·名称明度",
    "TakeLaneHeaderNameSaturation": "Take 通道·名称饱和度",
    "TakeLaneHeaderSaturation": "Take 通道·头部饱和度",
    "TakeLaneTrackHighlighted": "Take 通道（高亮）",
    "TakeLaneTrackNotHighlighted": "Take 通道（未高亮）",
    "TextDisabled": "禁用文字",
    "TextFrameSegmentBlendFactor": "文本分段框混合系数",
    "ThresholdLineColor": "阈值线",
    "ThresholdLineColorHover": "阈值线（悬停）",
    "TransportOffBackground": "走带按钮·关闭底色",
    "TransportOffDisabledForeground": "走带按钮·关闭+禁用",
    "TransportOffForeground": "走带按钮·关闭前景",
    "TransportProgress": "走带进度",
    "TransportSelectionBackground": "走带按钮·选中底色",
    "TreeColumnHeadBackground": "列表表头底色",
    "TreeColumnHeadControl": "列表表头控件",
    "TreeColumnHeadFocus": "列表表头焦点",
    "TreeColumnHeadForeground": "列表表头文字",
    "TreeColumnHeadSelected": "列表表头选中",
    "TreeRowCategoryBackground": "列表分类行底色",
    "TreeRowCategoryForeground": "列表分类行文字",
    "VelocityColor": "力度色",
    "VelocitySelectedOrHovered": "力度（选中/悬停）",
    "VelocityZoneBackground": "力度区底色",
    "VelocityZoneCrossfadeRamp": "力度区·交叉渐变",
    "ViewCheckControlDisabledOff": "开关控件·禁用(关)",
    "ViewCheckControlDisabledOn": "开关控件·禁用(开)",
    "ViewCheckControlEnabledOff": "开关控件·启用(关)",
    "ViewCheckControlEnabledOn": "开关控件·启用(开)",
    "ViewControlOff": "视图开关·关",
    "ViewControlOn": "视图开关·开",
    "WarperTimeBarMarkerBackground": "Warp 时间条·标记",
    "WarperTimeBarRulerBackground": "Warp 时间条·标尺",
    "WaveformColor": "波形色",
}

# 未知色值的兜底：按驼峰拆词再拼中文
_WORD_ZH = {
    "Control": "控件", "Background": "底色", "Foreground": "前景", "Frame": "边框",
    "Text": "文字", "Disabled": "禁用", "Hover": "悬停", "Selection": "选中",
    "Selected": "选中", "Standby": "待命", "Track": "轨道", "Lane": "通道",
    "Header": "头部", "Name": "名称", "Clip": "片段", "Slot": "槽位",
    "Grid": "网格", "Guideline": "辅助线", "Line": "线", "LineColor": "线色",
    "Markings": "刻度", "Ruler": "标尺", "Color": "颜色", "Alpha": "透明度",
    "Blend": "混合", "Factor": "系数", "Lightness": "明度", "Saturation": "饱和度",
    "Contrast": "对比", "Highlight": "高亮", "Shadow": "阴影", "Needle": "指针",
    "Meter": "电平表", "Curve": "曲线", "Outline": "描边", "Zone": "区域",
    "Ramp": "渐变", "Crossfade": "交叉渐变", "Piano": "钢琴", "Key": "键",
    "Black": "黑", "White": "白", "Separator": "分隔线", "Velocity": "力度",
    "Note": "音符", "Probability": "概率", "Automation": "自动化", "Transport": "走带",
    "Progress": "进度", "Scrollbar": "滚动条", "ScrollBar": "滚动条",
    "Handle": "手柄", "Inner": "内嵌", "Mixer": "混音台", "Browser": "浏览器",
    "Tag": "标签", "Item": "项目", "Sample": "采样", "Waveform": "波形",
    "Drum": "鼓", "Rack": "机架", "Scroller": "滚动条", "Pad": "垫",
    "Freeze": "冻结", "Gain": "增益", "Reduction": "衰减", "Threshold": "阈值",
    "Loop": "循环", "Scale": "音阶", "Awareness": "提示", "Session": "会话",
    "Tree": "列表", "Column": "列", "Head": "表头", "Category": "分类",
    "Search": "搜索", "Indication": "指示", "View": "视图", "Check": "勾选",
    "Range": "数值条", "EditField": "输入框", "Icon": "图标",
    "ContextMenu": "右键菜单", "Warper": "Warp", "TimeBar": "时间条",
    "Marker": "标记", "Spectrum": "频谱", "Alternative": "备选", "Default": "默认",
    "Alert": "警示", "Chosen": "按下", "Play": "播放", "Record": "录音",
    "PreListen": "预听", "Implicit": "隐式", "Linked": "关联", "Main": "主",
    "Focus": "焦点", "Indicator": "指示器", "Striped": "条纹", "Shade": "明暗",
    "Deactivated": "停用", "Muted": "静音", "Audition": "试听", "TakeLane": "Take 通道",
    "Inaudible": "不可听", "NonEditable": "不可编辑", "Expression": "表情",
    "Operator": "Operator", "Poti": "旋钮", "Bipolar": "双极", "Display": "显示",
    "RetroDisplay": "LCD 显示屏", "Surface": "表面", "SurfaceArea": "面板区域",
    "Preferences": "偏好设置", "Tab": "页签", "Desktop": "背景", "Button": "按钮",
}


def _split_camel(name):
    import re
    parts = re.findall(r"[A-Z][a-z0-9]*|[a-z0-9]+", name)
    return parts


def _compose(name):
    parts = _split_camel(name)
    words = [_WORD_ZH.get(p, "") for p in parts]
    words = [w for w in words if w]
    if not words:
        return ""
    return "".join(words)


def zh_for(name, section=None):
    """返回中文名；未知色值用拆词兜底，实在拼不出就返回空串。"""
    import re
    clip = re.match(r"^Clip(\d+)$", name)
    if clip:
        return "片段颜色 %s" % clip.group(1)
    seg = VU_SEGMENT_ZH.get(name)
    if seg:
        group = ""
        if section:
            for key, label in VU_GROUP_ZH.items():
                if key in section:
                    group = label
                    break
        return (group + "·" + seg) if group else seg
    hit = TOKEN_ZH.get(name)
    if hit:
        return hit
    return _compose(name)


def bilingual(name, section=None):
    """界面显示用：中文名 / 英文名。没有中文名时只给英文。"""
    zh = zh_for(name, section)
    return "%s / %s" % (zh, name) if zh else name
