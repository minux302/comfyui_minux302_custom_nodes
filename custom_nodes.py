from PIL import Image
import os
import numpy as np

# output_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../output")


class MySaveImage:
    def __init__(self):
        self.ouptut_dir = ""
        self.type = "output"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "filename": ("STRING", {"default": "MyComfyUI"}),
                "outdir": ("STRING", {"default": "output"}),
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "save_images"

    OUTPUT_NODE = True

    CATEGORY = "image"

    def save_images(self, images, outdir, filename):
        results = list()
        for count, image in enumerate(images):
            i = 255 * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            file = f"{filename}_{count:02}.png"
            img.save(os.path.join(outdir, file), compress_level=4)
            results.append(
                {
                    "filename": file,
                    # "subfolder": subfolder,
                    "type": self.type,
                }
            )

        return {"ui": {"images": results}}


class SaveConcatImage:
    def __init__(self):
        self.ouptut_dir = ""
        self.type = "output"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "filename": ("STRING", {"default": "MyComfyUI"}),
                "outdir": ("STRING", {"default": "output"}),
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "save_images"

    OUTPUT_NODE = True

    CATEGORY = "image"

    def _concat_imgs(self, imgs: list[Image.Image]) -> Image.Image:
        w, h = imgs[0].size
        num_imgs = len(imgs)
        dst = Image.new("RGB", (w * num_imgs, h))
        for i, img in enumerate(imgs):
            dst.paste(img, (w * i, 0))
        return dst

    def save_images(self, images, outdir, filename):
        results = list()
        file = f"{filename}.png"
        imgs = []
        for image in images:
            i = 255 * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            imgs.append(img)

        concat_img = self._concat_imgs(imgs)
        concat_img.save(os.path.join(outdir, file), compress_level=4)
        results.append({"filename": file, "type": self.type})

        return {"ui": {"images": results}}


NODE_CLASS_MAPPINGS = {
    "MySaveImage": MySaveImage,
    "SaveConcatImage": SaveConcatImage,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MySaveImage": "My Save Image",
    "SaveConcatImage": "Save Concat Image",
}
