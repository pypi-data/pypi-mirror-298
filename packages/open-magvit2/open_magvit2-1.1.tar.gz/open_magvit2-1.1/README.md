## OPEN-MAGVIT2 package

This is a fork of [OPEN-MAGVIT2: An Open-source Project Toward Democratizing Auto-Regressive Visual Generation](https://github.com/TencentARC/Open-MAGVIT2) in order to make it a package for easy usage.

## Install
```
pip install open-magvit2
```

## Example of usage

![reconstruction-examples](reconstruction-examples.png)

### 1. Download the checkpoint from huggingface
```bash
wget https://huggingface.co/TencentARC/Open-MAGVIT2/resolve/main/imagenet_256_L.ckpt
```
### 2. Load the model
```python
import pkg_resources
import torch
from omegaconf import OmegaConf
from open_magvit2.reconstruct import load_vqgan_new

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
config_path = pkg_resources.resource_filename('open_magvit2', 'configs/gpu/imagenet_lfqgan_256_L.yaml')
config = OmegaConf.load(config_path)
model = load_vqgan_new(config, "imagenet_256_L.ckpt").to(DEVICE)
```
### 3. Encode an image
```python
from PIL import Image
import torchvision.transforms as transforms

image = Image.open('1165.jpg')
image_tensor = transforms.ToTensor()(image)
batch = image_tensor.unsqueeze(0)
with torch.no_grad():
  quant, emb_loss, tokens, loss_breakdown = model.encode(image_tensor)
```
### 4. Decode
- decode from embeddings
```python
from open_magvit2.reconstruct import custom_to_pil

with torch.no_grad():
    tensor = model.decode(quant)

reconstructed_image = custom_to_pil(tensor[0])
```
- decode from tokens (i.e. ids)
```python
from einops import rearrange
from open_magvit2.reconstruct import custom_to_pil

x = rearrange(tokens, "(b s) -> b s", b=1)
q = model.quantize.get_codebook_entry(x, (1, 16, 16, 18), order='')

with torch.no_grad():
    tensor2 = model.decode(q)

reconstructed_image2 = custom_to_pil(tensor2[0])
```
### Example colab
Check this notebook [open-MAGVIT2-package-inference-example.ipynb](https://colab.research.google.com/drive/1lpqnekYG__GgSTmW2y7w4FZEZms54Sc5?usp=sharing)


