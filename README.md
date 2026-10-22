# BuildChecker：E6 / E7 课程实验

学号：241880465；A 组。代码基于 2026-10-20 课程学生实验包的 A-buildchecker 教学参考实现。

本仓库用于 E6 自动检测与修复复检，以及 E7 扩展测试、CI 和合并门禁演示。服务器原始主机信息、登录配置和登录凭据不上传。

## 运行

在有 Docker 的 Linux 环境、仓库根目录执行，每次重跑使用新的输出目录：

```bash
python3 scripts/lab_cloud.py build --out work/build-01 --build-timeout 1200
python3 scripts/lab_cloud.py e6 --out work/e6-before
python3 scripts/lab_cloud.py e6 --fixed --out work/e6-after
python3 scripts/verify_e6_evidence.py --before work/e6-before/evidence/findings.json --after work/e6-after/evidence/findings.json
python3 -m unittest discover -s tests/e7 -v
python3 scripts/lab_cloud.py gate --out work/e7-01
```

缺陷样例发现 MD(main.o, config.h) 和 RD(main.o, unused.h)，CLI 退出码 1 是预期结果。修复后应退出 0 且 findings 为空，仅 Makefile 输入哈希变化。

## 自主扩展测试

`services/buildchecker/tests/test_rename_output.py` 增加“临时产物重命名为最终目标”场景，检查最终目标、真实输入、临时文件排除和 rename 证据位置。该场景不在原有 15 项服务测试中。新增后预期 16 项通过；再加入课程门禁演示测试后预期 17 项通过。

## CI 与合并演示

工作流自动构建镜像、执行独立判定测试和完整门禁，并保留 artifact。`ci/A-main-protection.json` 为课程要求的保护配置；`ci/rejection-demo/A/` 提供故意错误与修正后的测试预期，仅用于证明失败 PR 被拦截、修正后恢复。

实际运行链接、失败拦截及已合并的 PR 记录见 [实验报告](docs/实验报告.md)。E6 前后校验、E7 八项门禁及恢复后的 17 项服务测试均已通过；云主机内存自检仍为 FAIL。


