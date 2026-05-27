# 道路巡检数据分析与报告系统 — 架构设计

## 1. 软件概述

本系统是"基于无人机的道路巡检系统"的数据后端软件，用于接收无人机采集的道路图像和GPS数据，通过AI模型自动识别道路病害（裂缝、坑洼、网裂等），进行统计分析，并生成标准化的巡检报告。

## 2. 技术选型

| 层级 | 技术 | 理由 |
|------|------|------|
| 后端框架 | Python Flask | 轻量、文档丰富、团队熟悉 |
| 数据库 | SQLite | 零配置、便携、适合单机部署 |
| 图像处理 | OpenCV | 行业标准、与YOLO无缝衔接 |
| AI检测 | YOLOv5 ONNX | 离线推理、不需要GPU |
| 前端 | Bootstrap 5 + Chart.js + Leaflet | 响应式、开源免费、无需API key |
| 报告输出 | HTML模板 → PDF | 可直接打印，格式可控 |
| 打包 | PyInstaller | 一键打包为exe |

## 3. 功能模块

### 3.1 数据导入模块
- 批量导入巡检图像（jpg/png/bmp）
- 导入GPS轨迹数据（CSV/GPX格式）
- 录入巡检元信息（日期、路段、操作员、天气等）
- 支持拖拽上传和文件对话框

### 3.2 图像预处理模块
- OpenCV去噪（高斯滤波/中值滤波）
- 边缘检测（Canny）
- 图像增强（直方图均衡化）
- 预处理前后对比展示

### 3.3 病害智能检测模块
- YOLOv5 ONNX模型推理
- 裂缝检测（横向/纵向/网状）
- 坑洼检测
- 病害位置标注（bounding box + GPS坐标映射）
- 严重程度分级（轻/中/重）

### 3.4 数据管理模块
- SQLite存储所有巡检记录
- 按日期、路段、病害类型检索
- 历史记录浏览和对比
- 数据导出（CSV/JSON）

### 3.5 可视化分析模块
- GPS轨迹地图展示（Leaflet）
- 病害分布热力图
- 统计图表：病害类型饼图、严重程度柱状图、月度趋势折线图
- 单次巡检详情面板

### 3.6 报告生成模块
- 标准化报告模板（HTML，支持打印）
- 报告内容：项目信息、巡检概况、病害清单、统计图表、养护建议
- 一键导出PDF/打印

## 4. 数据流

```
无人机采集 → 图像文件(.jpg) + GPS数据(.csv)
     ↓
[数据导入模块] → SQLite数据库
     ↓
[图像预处理] → 去噪/增强后的图像
     ↓
[YOLO病害检测] → 病害列表(类型+坐标+置信度+严重程度)
     ↓
[可视化分析] → 地图标注 + 统计图表
     ↓
[报告生成] → HTML报告 → PDF输出
```

## 5. 目录结构

```
road-inspection-system/
├── app.py                    # Flask主入口
├── config.py                 # 配置文件
├── models.py                 # SQLAlchemy数据模型
├── detector.py               # YOLO检测器封装
├── requirements.txt
├── modules/
│   ├── preprocess.py         # 图像预处理
│   ├── analysis.py           # 统计分析
│   └── report.py             # 报告生成
├── static/
│   ├── css/style.css
│   └── js/
│       ├── dashboard.js
│       ├── map.js
│       └── charts.js
├── templates/
│   ├── base.html
│   ├── index.html            # 首页仪表盘
│   ├── import_data.html      # 数据导入
│   ├── inspection_list.html  # 巡检记录列表
│   ├── inspection_detail.html # 单次巡检详情
│   ├── detect.html           # 病害检测
│   ├── analysis.html         # 统计分析
│   ├── map_view.html         # 地图视图
│   └── report.html           # 巡检报告
├── uploads/                  # 上传文件目录
├── reports/                  # 生成的报告
├── models/                   # YOLO模型文件
└── sample_data/              # 示例数据
```

## 6. 数据库设计

### inspections 表（巡检记录）
- id, title, road_section, inspector, date, weather, notes, created_at

### images 表（巡检图像）
- id, inspection_id(FK), filename, filepath, gps_lat, gps_lng, gps_alt, captured_at

### defects 表（病害记录）
- id, image_id(FK), inspection_id(FK), defect_type(crack/pothole/net_crack), severity(1-3), confidence, x, y, w, h, gps_lat, gps_lng, description

### gps_tracks 表（GPS轨迹）
- id, inspection_id(FK), point_order, lat, lng, alt, speed, timestamp
