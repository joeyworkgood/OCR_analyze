import os
import json

# === YOLO 的 label_map (固定 class id) ===
label_map = {
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
    '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14,
    'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19,
    'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24,
    'P': 25, 'Q': 26, 'R': 27, 'S': 28, 'T': 29,
    'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34,
    'Z': 35, 'Φ': 36, '-': 37
}

# === Labelme 錯誤標籤 (數字代碼 → 字母) ===
alias_map = {
    "10": "A", "11": "B", "12": "C", "13": "D", "14": "E",
    "15": "F", "16": "G", "17": "H", "18": "I", "19": "J",
    "20": "K", "21": "L", "22": "M", "23": "N", "24": "O",
    "25": "P", "26": "Q", "27": "R", "28": "S", "29": "T",
    "30": "U", "31": "V", "32": "W", "33": "X", "34": "Y",
    "35": "Z", "36": "Φ", "37": "-"
}

def convert_labelme_to_yolo(json_folder, save_folder):
    for file in os.listdir(json_folder):
        if file.endswith('.json'):
            json_path = os.path.join(json_folder, file)
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            image_width = data['imageWidth']
            image_height = data['imageHeight']
            yolo_lines = []

            for shape in data['shapes']:
                label = shape['label'].strip()

                
                if label in alias_map:
                    label = alias_map[label]

                
                if label not in label_map:
                    print(f"⚠️ 跳過無效標籤: {label}")
                    continue

                class_id = label_map[label]
                points = shape['points']

                
                if shape['shape_type'] == 'rectangle':
                    (x1, y1), (x2, y2) = points
                    x_min, x_max = min(x1, x2), max(x1, x2)
                    y_min, y_max = min(y1, y2), max(y1, y2)
                else:
                    x_coords = [p[0] for p in points]
                    y_coords = [p[1] for p in points]
                    x_min, x_max = min(x_coords), max(x_coords)
                    y_min, y_max = min(y_coords), max(y_coords)

               
                x_center = (x_min + x_max) / 2 / image_width
                y_center = (y_min + y_max) / 2 / image_height
                width = (x_max - x_min) / image_width
                height = (y_max - y_min) / image_height

                yolo_lines.append(
                    f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
                )

            
            os.makedirs(save_folder, exist_ok=True)
            txt_name = os.path.splitext(file)[0] + '.txt'
            txt_path = os.path.join(save_folder, txt_name)
            with open(txt_path, 'w') as out_file:
                out_file.write('\n'.join(yolo_lines))



convert_labelme_to_yolo(
    r"C:\ocr_git\OCR_analyze\j",
    r"C:\ocr_git\OCR_analyze\datasets\labels\val"
)


