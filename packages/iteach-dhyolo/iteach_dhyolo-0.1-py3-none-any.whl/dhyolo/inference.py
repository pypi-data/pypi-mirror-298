import torch
from iteach.dhyolo.detect import run

model_path = torch.load("/home/vinaya/Desktop/iteach/dhyolo/saved_models/best.pt")

run(
        weights = model_path,
        source = "/home/vinaya/Desktop/hololens/IRVLImageLabellingSupport/train_data/fetch.on.utd.campus.train.524/images/color_177.png"
    )