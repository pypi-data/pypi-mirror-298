import os

from rich.console import Console
from rich.table import Table

from src.api.settings import config
from src.api.utils.work_weixin_bot import send_text

# 创建一个表格
table = Table(title="Example Table")

table.add_column("门店编码", justify="right", style="cyan", no_wrap=True)
table.add_column("差异", style="magenta")
table.add_column("订单中心", justify="right", style="green")
table.add_column("dws", justify="right", style="green")

table.add_row("615032", "31.00", "392.36", "361.36")
table.add_row("158237", "29.43", "53.10", "23.67")
table.add_row("610126", "23.40", "358.60", "335.20")
table.add_row("318412", "22.69", "47.38", "24.69")
table.add_row("610033", "12.50", "56.30", "43.80")
table.add_row("371298", "11.90", "274.80", "262.90")
table.add_row("410642", "11.90", "59.50", "47.60")
table.add_row("140067", "9.90", "191.10", "181.20")
table.add_row("323179", "9.10", "161.06", "151.96")
table.add_row("140707", "7.60", "89.67", "82.07")

# 创建一个控制台对象
console = Console(record=True)
console.print(table)

# 获取脚本的完整路径
script_path = __file__

# 获取脚本所在的目录路径
script_dir = os.path.dirname(script_path)
# 将表格渲染为文本并导出
table_text = console.export_text()
print(table_text)

# # 获取脚本所在的目录路径
# script_dir = os.path.dirname(__file__)
# # 将 SVG 写入文件
# with open(script_dir + "/table_output.txt", "w", encoding="utf-8") as file:
#     file.write(table_text)

table_text = """
             Example Table
┏━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┳━━━━━━━━┓
┡━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━╇━━━━━━━━┩
│   615032 │ 31.00 │   392.36 │ 361.36 │
│   158237 │ 29.43 │    53.10 │  23.67 │
│   610126 │ 23.40 │   358.60 │ 335.20 │
│   318412 │ 22.69 │    47.38 │  24.69 │
│   610033 │ 12.50 │    56.30 │  43.80 │
│   371298 │ 11.90 │   274.80 │ 262.90 │
│   410642 │ 11.90 │    59.50 │  47.60 │
│   140067 │ 9.90  │   191.10 │ 181.20 │
│   323179 │ 9.10  │   161.06 │ 151.96 │
│   140707 │ 7.60  │    89.67 │  82.07 │
└──────────┴───────┴──────────┴────────┘
""".replace("   ", "\t")


send_text(config.wechat.wechat_data_quality, table_text, ["@李继聪"])
