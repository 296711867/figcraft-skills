// fig6-2 TensorRT 部署转换流程图（framework-v2）
// 用法：framework-v2.html#c=<本文件 base64url>&export=png&scale=2
@group 服务器端（RTX 3090） : dashed tl
pt tidy onnx
@end
@group Jetson Orin NX 端 : dashed tl
parse build opt engine fp32
@end

pt: PyTorch 训练权重 | （ACF-YOLO / ACF-YOLO-KD） @r1c1
tidy: 推理模型整理 | 融合 BN，保留一对一分支\n及端到端解码 @r1c2
onnx: ONNX 导出 | opset 13，静态输入\n1×3×640×640 → 1×300×6 @r1c3
parse: ONNX 解析 | 计算图 506 个节点\n均为标准算子 @r2c1
build: 构建配置 | FP16 精度标志\n工作空间 2 GB @r2c2 !blue
opt: 图优化与内核调优 | 层融合、精度选择\n逐层实测选内核 @r2c3 !blue
engine: 序列化引擎 | FP16 约 7.9 MB\n输出形状与数值校验 @r2c4 !blue
fp32: FP32 参考引擎（约 12.0 MB），用于数值一致性对照 @r3c2-3

pt -> tidy
tidy -> onnx
onnx -> parse
parse -> build
build -> opt
opt -> engine
build -> fp32
