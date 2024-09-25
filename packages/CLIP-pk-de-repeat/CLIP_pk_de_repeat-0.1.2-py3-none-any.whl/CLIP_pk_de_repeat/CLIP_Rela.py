#!python3
# coding=utf-8
"""
FilePath     : /main/CLIP_Rela.py
Description  : Compute image embedding by Clip
Author       : Ayleea zhengyalin@xiaomi.com
Date         : 2024-09-12 10:16:06
Version      : 0.0.1
"""
import json
import os
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from math import ceil
from pathlib import Path

import h5py
import numpy as np
import torch
# from torch.multiprocessing import Pool, set_start_method  
from PIL import Image
from transformers import CLIPModel, CLIPProcessor


# 从图片路径获取时间戳，车辆，相机
def get_timestamp_lable(file_path, is_stem=False):
    parts = file_path.split(":") if is_stem else Path(file_path).stem.split(":")
    return (
        datetime.fromtimestamp(int(parts[-1]) / 1e9),
        parts[3],
        parts[-2].split(".")[1] if parts[-2] != "bev" else parts[-2],
    )  # 时间戳，车辆，相机


def get_all_image_paths(root):
    """
    获取 root 文件夹下的所有图像路径。
    """
    image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
    image_paths = [str(p) for p in Path(root).rglob("*") if p.suffix.lower() in image_extensions]
    return image_paths


def divide_image_paths(image_paths, num_files=10):
    """
    将图像路径列表按数量分成 num_files 组。
    """
    total_images = len(image_paths)
    batch_size = ceil(total_images / num_files)

    # 分批次
    for i in range(0, total_images, batch_size):
        yield image_paths[i : i + batch_size]


def get_all_image_paths_by_camera_position(roots):
    """
    获取 roots 列表中所有文件夹的图像路径，并根据相机位置字段分类返回。
    :param roots: 包含多个文件夹路径的列表
    """
    image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
    image_paths_by_camera = defaultdict(list)
    for root in roots:  # 遍历多个文件夹
        for p in Path(root).rglob("*"):
            if p.suffix.lower() in image_extensions:
                image_path = str(p)
                camera_position = get_timestamp_lable(image_path)[-1]
                image_paths_by_camera[camera_position].append(image_path)

    return image_paths_by_camera


class CLIP_Emds:

    def __init__(self, clip_weights_path, device=None) -> None:
        self.clip_weights_path=clip_weights_path
        self.device = device if device is not None else ("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using {device} device: {torch.cuda.get_device_name(0)}")

    def _create_model_and_processor(self):
        """在每个线程中创建独立的模型和处理器实例"""
        model = CLIPModel.from_pretrained(self.clip_weights_path).to(self.device)
        processor = CLIPProcessor.from_pretrained(self.clip_weights_path)
        return model, processor
    
    # 为一张图片计算emd
    def compute_embedding(self, image_path):
        """
        计算单个图像的嵌入向量。
        """
        image_path = str(image_path)  
        try:
            # 在每个线程中创建独立的模型和处理器
            model, processor = self._create_model_and_processor()
            image = Image.open(image_path).convert("RGB")  
            inputs = processor(images=image, return_tensors="pt").to(self.device)  
            with torch.no_grad():
                embedding = model.get_image_features(**inputs)
            return embedding.cpu().numpy().flatten(), image_path
        except Exception as e:
            return None, image_path

    # 使用多线程为多个图片计算emd
    def compute_embeddings_parallel(self, image_paths, num_threads=8):
        """
        使用多线程计算所有图像的嵌入向量。
        return: emds {key:value}
        """
        results = {}
        error_images = []
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            for embedding, image_path in executor.map(self.compute_embedding, image_paths):
                if embedding is not None:
                    image_stem = Path(image_path).stem
                    results[image_stem] = embedding
                else:
                    error_images.append(image_path)
        return results, error_images

    # 使用多线程计算多个图片的emds，并使用h5文件增量保存
    def compute_embeddings_parallel_h5increment_save(
        self, image_paths, num_threads=8, batch_size=1000, output_file="output_embeddings.h5"
    ):
        """
        使用多线程计算所有图像的嵌入向量，按批次处理并增量存储。
        :param image_paths: 图像路径列表
        :param clip_weights_path: CLIP 模型权重路径
        :param num_threads: 并行线程数
        :param batch_size: 每批处理的图像数量
        :param output_file: 存储嵌入的输出文件
        """
        error_images = []
        total_images = len(image_paths)

        # 打开 HDF5 文件，准备增量存储
        with h5py.File(output_file, "a") as f:
            for i in range(0, total_images, batch_size):
                batch_paths = image_paths[i : min(i + batch_size, total_images)]
                batch_paths=[path for path in batch_paths if Path(path).stem not in f]
                if not batch_paths:
                    continue
                
                results = {}

                with ThreadPoolExecutor(max_workers=num_threads) as executor:
                    for embedding, image_path in executor.map(self.compute_embedding, batch_paths):
                        if embedding is not None:
                            image_stem = Path(image_path).stem
                            results[image_stem] = embedding
                        else:
                            error_images.append(image_path)

                # 将批次结果增量保存到 HDF5 文件
                for image_path, embedding in results.items():
                    if image_path not in f:
                        f.create_dataset(image_path, data=embedding, dtype="float32")

                print(f"Processed {min(i + batch_size, total_images)} of {total_images} images.")

        return error_images

    def compute_embeddings_for_multiple_h5files(
        self,
        dirs,
        num_threads=8,
        num_files=10,
        batch_size=1000,
        output_prefix="/parking-ssd/datasets/lmm/label_od_pld_fs/code/config/output_embeddings",
        error_log_prefix="/parking-ssd/datasets/lmm/label_od_pld_fs/code/error/error_log_",
    ):
        """
        对 dirs 目录下的所有图片进行嵌入计算，并分成 num_files 个 HDF5 文件存储。

        :param dirs: 多个图像根目录
        :param clip_weights_path: CLIP 模型权重路径
        :param num_threads: 并行线程数
        :param num_files: 生成的 HDF5 文件数量
        :param batch_size: 每批次处理图像数量
        :param output_prefix: 输出 HDF5 文件的前缀
        :param error_log_prefix: 输出图片emds抽取有问题的image path list
        """
        # 获取 root 目录下的所有图片路径
        image_paths = []
        for dir in dirs:
            image_paths.extend(get_all_image_paths(dir))
        # 将图像路径列表划分为 num_files 组
        divided_paths = list(divide_image_paths(image_paths, num_files=num_files))
        # print(divided_paths)
        # 遍历每一组，生成对应的 HDF5 文件
        for idx, image_paths_group in enumerate(divided_paths):
            output_file = f"{output_prefix}_{idx + 1}.h5"
            print(f"Processing file {idx + 1}/{num_files} -> {output_file}")

            # 调用批量处理并存储
            error_images = self.compute_embeddings_parallel_h5increment_save(
                image_paths=image_paths_group,
                num_threads=num_threads,
                batch_size=batch_size,
                output_file=output_file,
            )

            # 如果存在错误图像，则保存到 JSON 文件中
            if error_images:
                with open(error_log_prefix + str(idx + 1) + ".json", "w", encoding="utf-8") as f:
                    json.dump(error_images, f, indent=4, ensure_ascii=False)
            print(f"Completed file {idx + 1}/{num_files}. Errors: {len(error_images)}")

    def compute_embeddings_for_multiple_h5files_by_camera_position(
        self,
        dirs,
        num_threads=8,
        batch_size=1000,
        output_prefix="/parking-ssd/datasets/lmm/label_od_pld_fs/code/config/output_embeddings",
        error_log_prefix="/parking-ssd/datasets/lmm/label_od_pld_fs/code/error/error_log_",
    ):
        """
        对 dirs 目录下的所有图片进行多线程emds计算，并根据相机位置分类增量写入到不同的 HDF5 文件中。

        :param dirs: 图像根目录
        :param clip_weights_path: CLIP 模型权重路径
        :param num_threads: 并行线程数
        :param batch_size: 每批次处理的图像数量
        :param output_prefix: 输出 HDF5 文件的前缀
        :param error_log_prefix: 输出图片emds抽取有问题的image path list
        """
        # 获取 dirs 目录下的所有图片路径，并按相机位置分类
        image_paths_by_camera = get_all_image_paths_by_camera_position(dirs)
        # image_paths_by_camera = dirs
        print(f"Total cameras: {len(image_paths_by_camera)}", image_paths_by_camera.keys())
        # 对每个相机位置，生成对应的 HDF5 文件
        for camera_position, image_paths_group in image_paths_by_camera.items():
            output_file = f"{output_prefix}_{camera_position}.h5"
            print(f"Processing camera: {camera_position} -> {output_file}")

            # 调用批量处理并存储
            error_images = self.compute_embeddings_parallel_h5increment_save(
                image_paths=image_paths_group,
                num_threads=num_threads,
                batch_size=batch_size,
                output_file=output_file,
            )
            if error_images:
                with open(error_log_prefix + camera_position + ".json", "w", encoding="utf-8") as f:
                    json.dump(error_images, f, indent=4, ensure_ascii=False)
            print(f"Completed camera: {camera_position}. Errors: {len(error_images)}")

    # 使用增量的方式加载emds h5文件
    @staticmethod
    def load_embeddings_hdf5_increment(hdf5_file, chunk_size=1000):
        """
        增量读取 HDF5 文件，防止内存过载。

        :param hdf5_file: 文件路径
        :param chunk_size: 每次读取的键数量
        """
        embeddings = {}
        with h5py.File(hdf5_file, "r") as f:
            image_paths = list(f.keys())

            # 分批次读取，避免内存压力过大
            for i in range(0, len(image_paths), chunk_size):
                chunk_keys = image_paths[i : i + chunk_size]
                for image_path in chunk_keys:
                    embeddings[image_path] = f[image_path][:]  # 读取每个图像对应的嵌入向量

                # 模拟分块处理
                print(f"Loaded {i + len(chunk_keys)} of {len(image_paths)} embeddings.")

        return embeddings

    # 一次性保存emds到json文件
    @staticmethod
    def save_embeddings_json(embeddings, output_file):
        embeddings = {image_path: embedding.tolist() for image_path, embedding in embeddings.items()}
        with open(output_file, "w") as f:
            json.dump(embeddings, f)

    # 从json文件加载emds
    @staticmethod
    def load_embeddings_json(json_file):
        with open(json_file, "r") as f:
            embeddings = json.load(f)
        embeddings = {image_path: np.array(embedding, dtype="float32") for image_path, embedding in embeddings.items()}
        return embeddings

    # 一次性保存emds到h5文件
    @staticmethod
    def save_embeddings_hdf5(embeddings, output_file):
        with h5py.File(output_file, "w") as f:
            for image_path, embedding in embeddings.items():
                embedding = np.array(embedding, dtype="float32")
                # 将图像路径作为键，嵌入向量作为值
                f.create_dataset(image_path, data=embedding)

    # 从h5文件一次性加载全部emds
    @staticmethod
    def load_embeddings_hdf5(hdf5_file):
        embeddings = {}
        with h5py.File(hdf5_file, "r") as f:
            for image_path in f.keys():  # 遍历所有的图像路径
                embedding = f[image_path][:]  # 读取每个图像对应的嵌入向量
                embeddings[image_path] = embedding
        return embeddings

    # 保存emds到npz文件
    @staticmethod
    def save_embeddings_numpy(embeddings, output_file):
        # 将嵌入向量保存为 .npz 文件，使用 image_path 作为键
        np.savez_compressed(output_file, **embeddings)

    # 从npz文件加载emds
    @staticmethod
    def load_embeddings_numpy(npz_file):
        embeddings = {}
        data = np.load(npz_file, allow_pickle=True)  # 加载 .npz 文件
        for image_path in data.files:  # 遍历所有的图像路径
            embedding = data[image_path]  # 读取每个图像对应的嵌入向量
            embeddings[image_path] = embedding
        return embeddings


def print_hdf5_tree(group, prefix=""):
    """
    递归打印HDF5文件的结构树。
    :param group: 当前遍历到的HDF5组或文件对象
    :param prefix: 用于构建缩进的前缀字符串
    """
    # 打印当前组名（如果是根组，则不显示名称）
    if not isinstance(group, h5py.File):
        print(f"{prefix}+-- {group.name.split('/')[-1]}")

    # 遍历组中的所有项（包括子组和数据集）
    for name, obj in group.items():
        # 递归调用以打印子组的结构
        if isinstance(obj, h5py.Group):
            print_hdf5_tree(obj, prefix + "   ")
        # 打印数据集的名称（不包括数据类型和形状信息，以保持简洁）
        elif isinstance(obj, h5py.Dataset):
            shape = obj.shape if obj.shape else "()"  # 处理标量数据集
            dtype = obj.dtype.name
            print(f"{prefix}+-- {name} (dtype={dtype}, shape={shape})")


def restructure_hdf5_recursive(src_group, tgt_group, path=""):
    """
    递归地重构HDF5文件的一个组，将所有数据集移动到新组的根目录下，并以其路径的最后一个元素为键。

    :param src_group: 源HDF5文件中的组对象
    :param tgt_group: 目标HDF5文件中的组对象（用于存储重构后的数据）
    :param path: 当前在源HDF5文件中的路径（用于构建新键）
    """
    for name, obj in src_group.items():
        full_path = os.path.join(path, name) if path else name

        # 如果是数据集，则创建新键并复制数据
        if isinstance(obj, h5py.Dataset):
            new_key = Path(full_path).stem

            # 检查新键是否已存在于目标组中
            if new_key in tgt_group:
                print(f"新键 '{new_key}' 已存在于目标组中，跳过。。。")
                continue
            # 在目标组的根目录下创建新的数据集
            tgt_group.create_dataset(new_key, data=obj[:], dtype=obj.dtype)
            print(f"数据集已从 '{full_path}' 移动到目标组并重命名为 '{new_key}'。")

        # 如果是组，则递归调用
        elif isinstance(obj, h5py.Group):
            # 如果不需要保持子组的嵌套结构，可以直接在目标组的根目录下处理
            # 否则，你需要在目标组中创建对应的子组，并继续递归
            # 这里我们假设要展平所有结构，直接在目标组的根目录下处理
            restructure_hdf5_recursive(obj, tgt_group, full_path)


def restructure_hdf5(source_file, target_file):
    """
    重构HDF5文件，将所有数据集移动到新文件的根目录下，并以其路径的最后一个元素为键。

    :param source_file: 源HDF5文件的路径
    :param target_file: 目标HDF5文件的路径（用于存储重构后的数据）
    """
    # 使用h5py打开源HDF5文件和目标HDF5文件（如果目标文件已存在，则会被覆盖）
    with h5py.File(source_file, "r") as src_f, h5py.File(target_file, "w") as tgt_f:
        # 假设我们希望将所有数据移动到目标文件的根目录下
        # 你可以根据需要创建一个或多个子组来组织数据
        tgt_root = tgt_f  # 目标文件的根组

        # 递归遍历源文件的根组
        restructure_hdf5_recursive(src_f["/"], tgt_root)


if __name__ == "__main__":
    # 调用函数进行嵌入计算和保存
    dirs = [
        "/workspace/images-starfs/dataset/903/images/finetune/train_obstacle",
        "/workspace/images-starfs/workspace/xiabingquan/label_od_pld_fs/imgs/pld_img",
        "/workspace/images-starfs/workspace/xiabingquan/label_od_pld_fs/imgs/pld_img_0802",
        "/workspace/images-starfs/workspace/xiabingquan/label_od_pld_fs/imgs/pld_0903_rear_img",
    ]  # 设置根文件夹路径
    # dirs=['/parking-ssd/datasets/lmm/label_od_pld_fs/code/image/repeat']
    # dirs={
    # "rear_center_bottom_fish":["/workspace/images-starfs/workspace/xiabingquan/label_od_pld_fs/imgs/pld_0903_rear_img/rear_center_bottom_fish/adr::frame:eng.bhd.0039:cam.rear_center_bottom_fish.0:1686917339554184848.jpg"]
    # }
    clip_weights_path = "/workspace/images-starfs/workspace/zhengyalin/clip-vit-base-patch32"  # 设置 CLIP 权重路径，或者指定本地模型路径
    clip_emds_model=CLIP_Emds(clip_weights_path)
    clip_emds_model.compute_embeddings_for_multiple_h5files_by_camera_position(
        dirs=dirs,
        num_threads=16,
        output_prefix="/workspace/images-starfs/workspace/zhengyalin/pk_image_clip_embedding/new/pld_embeddings",
        error_log_prefix="/workspace/images-starfs/workspace/zhengyalin/pk_image_clip_embedding/error/pld_error_log_",
    )

    # 使用示例
    # ori_h5=Path('/workspace/images-starfs/workspace/zhengyalin/pk_image_clip_embedding/src_h5').glob('*.h5')
    # for hdf5_path in ori_h5:
    #     out_path=Path('/workspace/images-starfs/workspace/zhengyalin/pk_image_clip_embedding/rest_h5')/f'{hdf5_path.stem}_rest.h5'
    #     restructure_hdf5(hdf5_path,out_path)

    # with h5py.File(out_path, 'r') as of,h5py.File(hdf5_path,'r') as srcf:
    #     # print_hdf5_tree(srcf)
    #     print_hdf5_tree(of)
