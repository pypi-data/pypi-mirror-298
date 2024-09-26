import os

from playwright.sync_api import sync_playwright

from src.api.settings import config


def take_screenshot_sync(url, output_file):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.screenshot(path=output_file)
        browser.close()


# 获取脚本所在的目录路径
script_dir = os.path.dirname(__file__)

# 使用示例
take_screenshot_sync(
    "http://www.baidu.com",
    config.dirs.temp_path + "/example_screenshot_sync.png",
)
