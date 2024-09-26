#!python3
# coding=utf-8
"""
FilePath     : /main/PK_img_de_repeat.py
Description  : 为std-json中的图片去重
Author       : Ayleea zhengyalin@xiaomi.com
Date         : 2024-09-13 13:00:21
Version      : 0.0.1
"""
import json
import random
import shutil
from datetime import datetime
from pathlib import Path
from copy import deepcopy

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

from .CLIP_Rela import CLIP_Emds

default_pld_embeddings_dir = Path("/workspace/images-starfs/workspace/zhengyalin/pk_image_clip_embedding/new")
# 从std-json-->[{"image_key":path/to/image.jpg...}...]，获取全部图片路径  其中图片路径仅在使用“name-time”方式去重时可提供stem,否则需要使用全路径


def com_area_for_polygon(polygon):
    polygon = np.array(polygon)
    return 0.5 * np.abs(
        np.dot(polygon[:, 0], np.roll(polygon[:, 1], 1)) - np.dot(polygon[:, 1], np.roll(polygon[:, 0], 1))
    )


def compute_embeddings_for_Std_Json(
    std_json: "Std_Json",
    clip_emds_model: CLIP_Emds,
    image_key="image",
    save_embeddings_path=None,
    error_file=None,
    num_threads=8,
):
    images = [item[image_key] for item in std_json]
    embeddings, error_images = clip_emds_model.compute_embeddings_parallel(images, num_threads=num_threads)
    if error_file is not None and len(error_images) > 0:
        json.dump(error_images, open(error_file, "w", encoding="utf-8"), indent=4, ensure_ascii=False)
    print("cal emds error_images num:", len(error_images))

    if save_embeddings_path is not None:
        CLIP_Emds.save_embeddings_numpy(embeddings, save_embeddings_path)
    return embeddings


def set_image_root_dir_for_Std_Json(
    std_json: "Std_Json", image_root_dir: str or Path, image_key="image", is_remove=False
):
    image_root_dir = Path(image_root_dir) if isinstance(image_root_dir, str) else image_root_dir
    for item in std_json:
        if is_remove:
            item[image_key] = str(Path(item[image_key]).relative_to(image_root_dir))
        else:
            item[image_key] = str(image_root_dir / item[image_key])
    return std_json


def Std_Json_image_to_dir(std_json: "Std_Json", save_dir, image_key="image"):
    for item in std_json:
        image = Path(item[image_key])
        file_name = image.name
        save_path = Path(save_dir) / file_name
        save_path.parent.mkdir(parents=True, exist_ok=True)
        if not image.exists():
            print(image, "not exists!")
            continue
        shutil.copy(image, save_path)


# 从图片路径获取时间戳，车辆，相机
def get_timestamp_lable(file_path, is_stem=False):
    parts = file_path.split(":") if is_stem else Path(file_path).stem.split(":")
    return (
        datetime.fromtimestamp(int(parts[-1]) / 1e9),
        parts[3],
        parts[-2].split(".")[1] if parts[-2] != "bev" else parts[-2],
    )  # 时间戳，车辆，相机


class Std_Json:
    """
    形如[{}....]的json数据
    """

    def __init__(self, std_json=None):
        self.std_data = []
        if std_json:
            self.load(std_json)

    def load(self, std_json: "Std_Json" or list or dict or str or Path):
        if isinstance(std_json, Std_Json):
            self.std_data = deepcopy(std_json.std_data)
        elif isinstance(std_json, list):
            self.std_data = deepcopy(std_json)
        elif isinstance(std_json, str) or isinstance(std_json, Path):
            with open(std_json, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    self.std_data = data
                else:
                    raise TypeError("json file must be [{}..]")
        elif isinstance(std_json, dict):
            self.std_data = [std_json]
        else:
            raise TypeError("std_json must be Std_Json or list or dict or str or Path")

    def add(self, std_json):
        new_std_json = Std_Json(std_json)
        self.std_data.extend(new_std_json.std_data)

    def save(self, std_json_file):
        with open(std_json_file, "w", encoding="utf-8") as f:
            json.dump(self.std_data, f, ensure_ascii=False, indent=4)

    def sort_by_key_word(self, key_word, reverse=False):
        self.std_data.sort(key=lambda x: get_timestamp_lable(x[key_word])[0], reverse=reverse)
        # self.std_data.sort(key=lambda x: x[key_word], reverse=reverse)

    def remove(self, index):
        self.std_data.remove(index)

    def copy(self):
        copy_std_json = Std_Json(self)
        return copy_std_json

    def __add__(self, other: "Std_Json"):
        sum_std_json = Std_Json()
        sum_std_json.std_data = deepcopy(self.std_data)
        sum_std_json.std_data.extend(other.std_data)
        return sum_std_json

    def __sub__(self, other: "Std_Json"):
        ori_str_data=[json.dumps(item, sort_keys=False) for item in self.std_data]
        for item in other.std_data:
            str_item=json.dumps(item, sort_keys=False)
            if str_item in ori_str_data:
                ori_str_data.remove(str_item)
        sub_std_data=[json.loads(item) for item in ori_str_data]
        return Std_Json(sub_std_data)

    def __len__(self):
        return len(self.std_data)

    def __getitem__(self, index):
        return self.std_data[index]

    def __iter__(self):
        # 返回迭代器对象
        return iter(self.std_data)


# 这里要求std json形如：[{image_key:"xxx.jpg",...}....]
class Cls_Sorted_Json:  # 统计的全部obj都是有效的（is_visible=True）;imgae都是在本机存在的
    def __init__(self, cls_Sorted_json=None, image_key: str = "image"):
        self.image_key = image_key

        self.car_model_set = set()
        self.cls_sorted_data = {}

        self.item_count = 0
        self.image_set = set()

        if cls_Sorted_json:
            self.load(cls_Sorted_json)

    def load(self, json_data: "Cls_Sorted_Json" or Std_Json or str or Path or dict or list):

        if isinstance(json_data, Std_Json):
            self.load_by_std_json(json_data)

        elif isinstance(json_data, list):
            self.load_by_std_json(Std_Json(json_data))

        elif isinstance(json_data, dict):
            self.cls_sorted_data = json_data
            self.update()

        elif isinstance(json_data, str) or isinstance(json_data, Path):
            temp_data = json.load(open(json_data, "r", encoding="utf-8"))
            self.load(temp_data)

        elif isinstance(json_data, "Cls_Sorted_Json"):
            self.cls_sorted_data = json_data.cls_sorted_data.copy()
            self.car_model_set = json_data.car_model_set.copy()
            self.image_set = json_data.image_set.copy()
            self.item_count = json_data.item_count
            self.image_key = json_data.image_key
        else:
            raise TypeError("json_data must be Std_Json or str or Path or dict or list")

    def load_by_std_json(self, std_json: Std_Json, image_key: str = None):
        if not image_key is None:
            self.image_key = image_key
        for item in std_json:
            image_file = item[self.image_key]
            timestamp, model, cam = get_timestamp_lable(image_file)
            if model not in self.cls_sorted_data:
                self.cls_sorted_data[model] = {}
            if cam not in self.cls_sorted_data[model]:
                self.cls_sorted_data[model][cam] = Std_Json()

            self.cls_sorted_data[model][cam].add(item)

        self.update()

        return self.cls_sorted_data

    def update(self):

        self.car_model_set = set(self.cls_sorted_data.keys())
        self.item_count = 0
        self.image_set = set()

        for model, model_dict in self.cls_sorted_data.items():
            for cam, items in model_dict.items():
                self.item_count += len(items)
                # 确保可以加载dict
                if not isinstance(items, Std_Json):
                    model_dict[cam] = Std_Json(items)

                model_dict[cam].sort_by_key_word(self.image_key, reverse=False)
                for item in items:
                    self.image_set.add(item[self.image_key])

    def save(self, json_path):
        save_cls_sorted_data = self.cls_sorted_data.copy()
        for model, model_dict in save_cls_sorted_data.items():
            for cam, items in model_dict.items():
                model_dict[cam] = list(items)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(save_cls_sorted_data, f, indent=4, ensure_ascii=False)

    def De_repeat_for_cls_sorted_json(
        self, De_repeat_mode="clip-cos-sim", save_sim_img_dir=None, save_repeat_img_dir=None, **kwargs
    ):
        """
        :param De_repeat_mode: 去重模式，默认为"clip-cos-sim"
        """
        for model, model_dict in self.cls_sorted_data.items():
            for cam, items in model_dict.items():
                if De_repeat_mode.lower() == "name-time":
                    model_dict[cam] = Cls_Sorted_Json.de_repeat_by_name_time(items, image_key=self.image_key, **kwargs)
                elif De_repeat_mode.lower() == "clip-cos-sim":
                    model_dict[cam], sim_img_std_json, repeat_img_std_json = (
                        Cls_Sorted_Json.de_repeat_by_CLIP_embedding_cos_sim(
                            items, image_key=self.image_key, car_model=model, cam=cam, **kwargs
                        )
                    )
                    if save_sim_img_dir is not None:
                        Std_Json_image_to_dir(sim_img_std_json, save_sim_img_dir)
                    if save_repeat_img_dir is not None:
                        Std_Json_image_to_dir(repeat_img_std_json, save_repeat_img_dir)
                elif De_repeat_mode.lower() == "clip-kmeans":
                    pass
                else:
                    raise ValueError("De_repeat_mode must be 'name-time' or 'clip-cos-sim' or 'clip-kmeans'")

    @staticmethod
    def de_repeat_by_name_time(items: Std_Json, image_key="image", time_window=5, step=0):
        """
        对items进行去重，根据name-time的方式去重
        :param items: 一个按照时间戳排好序的同个车辆、同一个cam的list，每个元素是一个dict，包含image key属性即：sorted[{'image': 'timestamp.jpg'...}...]
        :param image_key: 图片路径的key，默认为“image”
        :return: 去重后的items
        """
        print("\n原有数据时间戳个数：", len(items))
        unique_items = Std_Json()
        temp_list = []
        for timestamp_image_dict in tqdm(items, desc="去重中"):
            if len(unique_items) == 0:
                unique_items.add(timestamp_image_dict)
                continue

            timestamp = get_timestamp_lable(timestamp_image_dict[image_key])[0]
            unique_last_timestamp = get_timestamp_lable(unique_items[-1][image_key])[0]

            if abs((unique_last_timestamp - timestamp).total_seconds()) < time_window:
                temp_list.append(timestamp_image_dict)
            else:
                if step > 1:
                    temp_list = temp_list[::step]
                elif 0 < step < 1:
                    temp_list = random.sample(temp_list, int(len(temp_list) * step))
                elif step == 0:
                    temp_list = []
                temp_list.append(timestamp_image_dict)
                unique_items.add(temp_list)
                temp_list = []
        # 处理最后一部分在temp中的数据
        if len(temp_list) > 0:
            if step > 1:
                temp_list = temp_list[::step]
            elif 0 < step < 1:
                temp_list = random.sample(temp_list, int(len(temp_list) * step))
            elif step == 0:
                temp_list = []
            unique_items.add(temp_list)

        print("去重后数据时间戳个数：", len(unique_items))
        return unique_items

    @staticmethod
    def de_repeat_for_Std_Json_by_embeddings(  # TODO 可优化Faiss包的使用
        items: list, embeddings_dict: dict, image_key="image", cos_sim_threshold=0.95, choice_max_area=False
    ):
        unique_images = []
        sim_images = set()
        repeat_images = []
        emds_lack_num = 0

        if choice_max_area:
            items.sort(key=lambda item: com_area_for_polygon(item["polygon"]))

        temp_items = items.copy()
        embeddings = []
        for i, item in enumerate(temp_items):
            img_key = item[image_key]
            embedding = embeddings_dict.get(Path(img_key).stem, None)
            if embedding is None:
                # 如果嵌入向量不存在，直接添加到unique_images
                # unique_images.append(item)
                items.remove(item)
                emds_lack_num += 1
                # del items[i]
            else:
                # 否则，添加到embeddings列表中
                embeddings.append(embedding)

        # 如果embeddings为空，则无需计算相似度，直接返回
        if not embeddings:
            return unique_images, [], repeat_images, emds_lack_num

        embeddings = np.array(embeddings)

        if len(embeddings) != len(items):
            # debug
            # print(embeddings.shape,len(items))
            raise ValueError("The number of embeddings does not match the number of items.")

        sim_matrix = cosine_similarity(embeddings)
        # print(sim_matrix.max(), sim_matrix.min())

        for i, _ in enumerate(embeddings):
            # 假设当前图片是唯一的，直到找到更相似的图片
            is_unique = True
            # 检查当前图片与其他所有图片的相似度
            for j in range(i + 1, len(embeddings)):
                if sim_matrix[i, j] >= cos_sim_threshold:
                    # 如果找到相似度高于阈值的图片，则标记当前图片为非唯一
                    is_unique = False
                    break
            # 如果当前图片是唯一的，则添加到结果列表中
            if is_unique:
                unique_images.append(items[i])
            else:
                repeat_images.append(items[i])

                sim_images.add(json.dumps(items[i], sort_keys=True))
                sim_images.add(json.dumps(items[j], sort_keys=True))
        return unique_images, [json.loads(item) for item in sim_images], repeat_images, emds_lack_num

    @staticmethod
    def de_repeat_by_CLIP_embedding_cos_sim(
        items: Std_Json,
        car_model="eng.bhd.0039",
        cam="front_center_bottom_fish",
        cos_sim_threshold=0.95,
        image_key="image",
        time_window=60,
        choice_max_area=False,
        embeddings=None,
    ):
        if choice_max_area:
            print("***************choice polygon with max area****************")
        # TODO 根据 car_model and cam在h5文件中取值
        if embeddings is None:
            print("***************use default embeddings****************")
            embeddings_dict = CLIP_Emds.load_embeddings_hdf5(
                Path(default_pld_embeddings_dir) / f"pld_embeddings_{cam}.h5"
            )
        else:
            print("***************use diy embeddings****************")
            embeddings_dict = embeddings

        print("原有数据个数：", len(items))

        unique_items = Std_Json()
        sim_items = Std_Json()
        repeat_items = Std_Json()
        emds_lack_num = 0

        temp_list = []
        for timestamp_image_dict in tqdm(items, desc=f"{car_model}->{cam}去重中"):
            if len(temp_list) == 0:
                temp_list.append(timestamp_image_dict)
                continue

            timestamp = get_timestamp_lable(timestamp_image_dict[image_key])[0]
            unique_last_timestamp = get_timestamp_lable(temp_list[0][image_key])[0]

            if abs((unique_last_timestamp - timestamp).total_seconds()) < time_window:
                temp_list.append(timestamp_image_dict)
            else:
                if len(temp_list) > 1:
                    temp_list, sim_list, repeat_list, emds_lack = Cls_Sorted_Json.de_repeat_for_Std_Json_by_embeddings(
                        temp_list, embeddings_dict, image_key, cos_sim_threshold, choice_max_area=choice_max_area
                    )
                    sim_items.add(sim_list)
                    repeat_items.add(repeat_list)
                    emds_lack_num += emds_lack
                unique_items.add(temp_list)
                temp_list = [timestamp_image_dict]

        if len(temp_list) > 1:
            temp_list, sim_list, repeat_list, emds_lack = Cls_Sorted_Json.de_repeat_for_Std_Json_by_embeddings(
                temp_list, embeddings_dict, image_key, cos_sim_threshold, choice_max_area=choice_max_area
            )
            sim_items.add(sim_list)
            repeat_items.add(repeat_list)
            emds_lack_num += emds_lack
        unique_items.add(temp_list)

        print(
            f"去重后数据个数：{len(unique_items)}; 重复的数据的数据个数：{len(repeat_items)}; 重复率：{len(repeat_items)/len(items)}; embedding lack:{emds_lack_num}\n"
        )
        return unique_items, sim_items, repeat_items

    def add(self, std_json):
        pass

    def to_std_json(self):
        res_std_json = Std_Json()
        for model, model_dict in self.cls_sorted_data.items():
            for cam, items in model_dict.items():
                res_std_json.add(items)
        return res_std_json

    def image_to_dir(self, dir_path):
        Std_Json_image_to_dir(self.to_std_json(), dir_path)

    def __add__(self, other):
        pass

    def __len__(self):
        return self.item_count

    def __getitem__(self, indexs: list or str):
        if isinstance(indexs, str):
            return self.cls_sorted_data[indexs]
        else:
            res = self.cls_sorted_data[indexs[0]]
            for index in indexs[1:]:
                res = res[index]
            return res

    def __iter__(self):
        # 返回迭代器对象
        return iter(self.cls_sorted_data)


def de_repeat_for_std_json_file(
    ori_std_json_file,
    de_repeat_std_json_file,
    save_ori_img_dir=None,
    save_de_repeat_img_dir=None,
    image_root_dir=None,
    **kwargs,
):

    std_json = Std_Json(ori_std_json_file)

    if image_root_dir is not None:
        std_json = set_image_root_dir_for_Std_Json(std_json=std_json, image_root_dir=image_root_dir)

    if save_ori_img_dir:
        Std_Json_image_to_dir(std_json, save_ori_img_dir)

    cls_sorted_json = Cls_Sorted_Json(std_json)

    cls_sorted_json.De_repeat_for_cls_sorted_json(**kwargs)

    res_json = cls_sorted_json.to_std_json()
    if save_de_repeat_img_dir:
        Std_Json_image_to_dir(res_json, save_de_repeat_img_dir)

    if image_root_dir is not None:
        res_json = set_image_root_dir_for_Std_Json(std_json=res_json, image_root_dir=image_root_dir, is_remove=True)

    res_json.save(de_repeat_std_json_file)

    print(
        f"数据总量：{len(std_json)}; 去重后数据量：{len(res_json)}; 重复率：{(len(std_json)-len(res_json))/len(std_json)}"
    )


if __name__ == "__main__":
    # CLIP权重文件夹位置
    clip_weights = "/workspace/images-starfs/workspace/zhengyalin/clip-vit-base-patch32"
    #去重模式、时间窗、余弦相似度阈值、是否选择最大的polygon面积
    de_repeat_mode="clip-cos-sim"
    time_window = 60
    cos_sim_threshold = 0.95
    choice_max_area = True
    # 需要去重的std_json文件相关设置
    std_json_file = Path("/workspace/images-starfs/workspace/zhengyalin/COT/parking_space_waibao/0924-41550/0924-41550_cot.json")
    de_repeat_std_json_file = std_json_file.with_name(std_json_file.stem + "_de_repeat.json")
    save_ori_img_dir = None  # f"image/{std_json_file.stem}_ori_{time_window}_{cos_sim_threshold}",
    save_de_repeat_img_dir =None  # f"image/{std_json_file.stem}_de_repeat_{time_window}_{cos_sim_threshold}"
    save_sim_img_dir = None  # f"image/{std_json_file.stem}_sim_{time_window}_{cos_sim_threshold}"
    save_repeat_img_dir = None  # f"image/{std_json_file.stem}_repeat_{time_window}_{cos_sim_threshold}"

    image_root_dir = None  # "/workspace/images-starfs/dataset"

    # 需要计算emds的相关参数
    Calculation_emds = False
    use_emds_file = (
        f"/workspace/images-starfs/workspace/zhengyalin/pk_image_clip_embedding/{std_json_file.stem}_pld_embeddings.npz"
    )
    cal_emds_error_file = (
        f"/workspace/images-starfs/workspace/zhengyalin/pk_image_clip_embedding/error/{std_json_file.stem}_error.json"
    )

    # 计算emds
    emds = None
    if Calculation_emds:
        std_json = Std_Json(std_json_file)
        if image_root_dir:
            std_json = set_image_root_dir_for_Std_Json(std_json=std_json, image_root_dir=image_root_dir)

        if not Path(use_emds_file).exists():
            clip_emds_model = CLIP_Emds(clip_weights_path=clip_weights)
            emds = compute_embeddings_for_Std_Json(
                std_json=std_json,
                clip_emds_model=clip_emds_model,
                image_key="image",
                save_embeddings_path=use_emds_file,
                error_file=cal_emds_error_file,
                num_threads=8,
            )
        else:
            emds = CLIP_Emds.load_embeddings_numpy(use_emds_file)

    # 为std_json文件中image去重
    de_repeat_for_std_json_file(
        ori_std_json_file=std_json_file,
        de_repeat_std_json_file=de_repeat_std_json_file,
        save_ori_img_dir=save_ori_img_dir,
        save_de_repeat_img_dir=save_de_repeat_img_dir,
        image_root_dir=image_root_dir,
        De_repeat_mode=de_repeat_mode,
        save_sim_img_dir=save_sim_img_dir,
        save_repeat_img_dir=save_repeat_img_dir,
        choice_max_area=choice_max_area,
        time_window=time_window,
        cos_sim_threshold=cos_sim_threshold,
        embeddings=emds,
    )