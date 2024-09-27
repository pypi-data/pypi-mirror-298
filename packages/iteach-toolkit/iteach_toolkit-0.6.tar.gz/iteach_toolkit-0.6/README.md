# iTeach DHYOLO Package

## Overview

The `iTeach_package` package provides functionalities for running YOLOv5 object detection to identify doors and handles in images. Thus package deals with inference using Yolov5 model. This package includes command-line tools for inference with YOLOv5.

## Model Checkpoints

Download the pretrained checkpoints from [here](https://utdallas.box.com/v/DHYOLO-Pretrained-Checkpoints).

## Install

```shell
pip install iteach_toolkit
```

## Usage

```python
from DHYOLO import DHYOLODetector  # or from dhyolo if keeping the original name

# Set up paths
image_path = "./test_imgs/irvl-test.jpg"
model_path = "path/to/yolov5_model.pt"

# Initialize the Predict class
dhyolo = DHYOLODetector(model_path)

# Run inference
dhyolo.predict(image_path)
```