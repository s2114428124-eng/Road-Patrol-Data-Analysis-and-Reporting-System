"""
生成用于测试的模拟道路图像
包含不同类型的模拟病害：裂缝、坑洼、网状裂缝
"""
import cv2
import numpy as np
import os
import random

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'sample_data', 'test_images')
os.makedirs(OUTPUT_DIR, exist_ok=True)

IMG_WIDTH, IMG_HEIGHT = 800, 600


def create_road_background():
    """创建灰色道路背景"""
    img = np.ones((IMG_HEIGHT, IMG_WIDTH, 3), dtype=np.uint8) * 180
    # 添加道路纹理噪声
    noise = np.random.randint(-15, 15, (IMG_HEIGHT, IMG_WIDTH), dtype=np.int16)
    for c in range(3):
        channel = img[:, :, c].astype(np.int16) + noise
        img[:, :, c] = np.clip(channel, 0, 255).astype(np.uint8)
    # 路面标线
    for y in range(IMG_HEIGHT):
        if abs(y % 120 - 60) < 3:
            img[y, IMG_WIDTH//4:3*IMG_WIDTH//4] = [230, 230, 230]
    return img


def add_crack(img, x, y, length, angle, width=2):
    """添加裂缝"""
    end_x = int(x + length * np.cos(np.radians(angle)))
    end_y = int(y + length * np.sin(np.radians(angle)))
    # 随机曲折
    points = []
    num_segments = max(length // 20, 3)
    for i in range(num_segments + 1):
        t = i / num_segments
        px = int(x + (end_x - x) * t + random.randint(-8, 8))
        py = int(y + (end_y - y) * t + random.randint(-8, 8))
        px = np.clip(px, 0, IMG_WIDTH - 1)
        py = np.clip(py, 0, IMG_HEIGHT - 1)
        points.append((px, py))

    for i in range(len(points) - 1):
        cv2.line(img, points[i], points[i + 1], (30, 30, 30), max(width + random.randint(-1, 1), 1))

    # 裂缝边缘加深
    for i in range(len(points) - 1):
        cv2.line(img, points[i], points[i + 1], (10, 10, 10), max(width - 1, 1))


def add_pothole(img, cx, cy, radius):
    """添加坑洼"""
    # 暗色圆形区域
    overlay = img.copy()
    cv2.circle(overlay, (cx, cy), radius, (25, 25, 25), -1)
    cv2.circle(overlay, (cx, cy), radius + 2, (40, 40, 40), 2)
    # 内部纹理
    for _ in range(radius * 2):
        rx = cx + random.randint(-radius, radius)
        ry = cy + random.randint(-radius, radius)
        if (rx - cx) ** 2 + (ry - cy) ** 2 < radius ** 2:
            cv2.circle(overlay, (rx, ry), 1, (15, 15, 15), -1)
    # 半透明混合
    alpha = 0.85
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)


def add_net_crack(img, cx, cy, size):
    """添加网状裂缝"""
    num_lines = random.randint(8, 15)
    for _ in range(num_lines):
        angle = random.uniform(0, 360)
        length = random.randint(size // 2, size)
        ex = int(cx + length * np.cos(np.radians(angle)))
        ey = int(cy + length * np.sin(np.radians(angle)))
        ex = np.clip(ex, 0, IMG_WIDTH - 1)
        ey = np.clip(ey, 0, IMG_HEIGHT - 1)
        cv2.line(img, (cx, cy), (ex, ey), (20, 20, 20), random.randint(1, 2))

    # 交叉线
    for _ in range(num_lines // 2):
        sx = cx + random.randint(-size // 2, size // 2)
        sy = cy + random.randint(-size // 2, size // 2)
        ex = sx + random.randint(-size // 3, size // 3)
        ey = sy + random.randint(-size // 3, size // 3)
        cv2.line(img, (sx, sy), (ex, ey), (25, 25, 25), 1)


def generate_images():
    """生成多种类型的测试图像"""
    seed = 42
    random.seed(seed)
    np.random.seed(seed)

    # 1. 正常路面（少量微小裂缝）
    img = create_road_background()
    add_crack(img, 200, 300, 60, 15, 1)
    cv2.imwrite(os.path.join(OUTPUT_DIR, 'road_normal.jpg'), img)
    print(f"生成: road_normal.jpg (正常路面，微小裂缝)")

    # 2. 横向裂缝
    img = create_road_background()
    add_crack(img, 100, 250, 300, 5, 3)
    add_crack(img, 150, 400, 250, 8, 2)
    cv2.imwrite(os.path.join(OUTPUT_DIR, 'road_crack_h.jpg'), img)
    print(f"生成: road_crack_h.jpg (横向裂缝)")

    # 3. 纵向裂缝
    img = create_road_background()
    add_crack(img, 300, 50, 250, 85, 3)
    add_crack(img, 500, 100, 300, 92, 2)
    cv2.imwrite(os.path.join(OUTPUT_DIR, 'road_crack_v.jpg'), img)
    print(f"生成: road_crack_v.jpg (纵向裂缝)")

    # 4. 网状裂缝
    img = create_road_background()
    add_net_crack(img, 300, 250, 120)
    add_net_crack(img, 550, 400, 80)
    cv2.imwrite(os.path.join(OUTPUT_DIR, 'road_net_crack.jpg'), img)
    print(f"生成: road_net_crack.jpg (网状裂缝)")

    # 5. 坑洼
    img = create_road_background()
    add_pothole(img, 250, 300, 45)
    add_pothole(img, 500, 200, 35)
    add_pothole(img, 600, 450, 50)
    cv2.imwrite(os.path.join(OUTPUT_DIR, 'road_pothole.jpg'), img)
    print(f"生成: road_pothole.jpg (坑洼)")

    # 6. 综合病害（多种病害混合）
    img = create_road_background()
    add_crack(img, 100, 150, 200, 10, 2)
    add_pothole(img, 350, 300, 40)
    add_net_crack(img, 600, 250, 100)
    add_crack(img, 200, 450, 150, 80, 2)
    add_pothole(img, 550, 480, 30)
    cv2.imwrite(os.path.join(OUTPUT_DIR, 'road_mixed.jpg'), img)
    print(f"生成: road_mixed.jpg (综合病害)")

    # 7-10: 额外的随机图像
    for i in range(7, 11):
        img = create_road_background()
        defect_type = random.choice(['crack_h', 'crack_v', 'pothole', 'net_crack'])
        if defect_type == 'crack_h':
            for _ in range(random.randint(1, 3)):
                add_crack(img, random.randint(50, 600), random.randint(80, 500),
                          random.randint(60, 300), random.randint(-10, 10), random.randint(1, 3))
        elif defect_type == 'crack_v':
            for _ in range(random.randint(1, 3)):
                add_crack(img, random.randint(100, 700), random.randint(30, 200),
                          random.randint(60, 300), random.randint(80, 100), random.randint(1, 3))
        elif defect_type == 'pothole':
            for _ in range(random.randint(1, 4)):
                add_pothole(img, random.randint(100, 700), random.randint(100, 500),
                            random.randint(20, 55))
        elif defect_type == 'net_crack':
            add_net_crack(img, random.randint(150, 650), random.randint(150, 450),
                          random.randint(60, 130))

        cv2.imwrite(os.path.join(OUTPUT_DIR, f'road_sample_{i}.jpg'), img)
        print(f"生成: road_sample_{i}.jpg")

    print(f"\n共生成 10 张测试图像，保存在: {OUTPUT_DIR}")


if __name__ == '__main__':
    generate_images()