# 安装说明


## 安装 rye

``` shell
curl -sSf https://rye-up.com/get | bash
rye self update
```

## 创建项目

``` shell
rye init jcutils --build-system maturin
cd jcutils
rye pin 3.11.1
```

## 安装环境

``` shell
cd jcutils
rye sync
rye run serve #启动
rye sync --no-lock
```

## rye使用

```shell
# 安装依赖
rye sync
# 代码检查
rye lint
rye lint --fix
# 格式化代码
rye fmt
# 测试
rye test
# 打包 （包含 rust 扩展打包）
rye build
# 发布
rye publish
# rust扩展包快速打包
maturin develop --skip-install
```

## 代码覆盖率检测

```shell
# 运行测试并收集覆盖率数据：
coverage run -m pytest

# 单个文件覆盖率报告：
coverage run -m pytest tests/test_coverage.py

# 生成覆盖率报告
coverage report

# 生成 HTML 报告（可选）
coverage html

# 查看详细报告：
coverage report -m

```

## docker方式部署命令参考

```shell
# 尽量在linux下 build，避免架构不一致

docker build -f Dockerfile -t guoquan-apocalypse-cron .
docker run -d -p 15603:15603 -e ENV=dev --name guoquan-apocalypse-cron guoquan-apocalypse-cron
docker run -d -p 15603:15603 -e ENV=test --name guoquan-apocalypse-cron guoquan-apocalypse-cron
docker run -d -p 15603:15603 -e ENV=prod --name guoquan-apocalypse-cron guoquan-apocalypse-cron
```


