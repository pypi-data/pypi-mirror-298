import os
from typing import Tuple
import cv2, numpy as np


class OpencvHelper:
    @staticmethod
    def gen_random_img(width: int, height: int, item=3) -> cv2.typing.MatLike:
        """
        生成随机图片
        :param width: 整形数 宽
        :param height: 整形数:高
        :param item: 整形数:通道数
        :return: NDArray: 随机生成的图片
        """
        # 生成一个宽为width，高为height，通道数为item的随机整数数组
        img = np.random.randint(0, 255, (width, height, item))
        # 将数组类型转换为uint8
        img = img.astype(np.uint8)
        # 返回生成的图片
        return img

    @staticmethod
    def color_to_range(color: str, sim: int) -> Tuple[Tuple[int, ...], Tuple[int, ...]]:
        """
        根据给定的颜色和相似度参数，计算出一个颜色范围的下限和上限
        :param color: 字符串:颜色 ffffff-303030 或者 ffffff
        :param sim: 整形数:相似度 小于等于1
        :return: (lower, upper): 上限和下限元组
        """
        # 转换大漠格式RGB "ffffff-303030" 为 BGR遮罩范围(100,100,100),(255,255,255)
        if sim > 1:
            raise "参数错误"
        # 判断color的长度是否为6
        if len(color) == 6:
            # 将color赋值给c，将"000000"赋值给weight
            c = color
            weight = "000000"
        # 判断color中是否包含"-"
        elif "-" in color:
            # 将color按照"-"分割，将分割后的第一个值赋值给c，将分割后的第二个值赋值给weight
            c, weight = color.split("-")
        else:
            raise "参数错误"
        # 将c按照16进制转换为整数，分别赋值给color的三个值
        color = int(c[4:], 16), int(c[2:4], 16), int(c[:2], 16)
        # 将weight按照16进制转换为整数，分别赋值给weight的三个值
        weight = int(weight[4:], 16), int(weight[2:4], 16), int(weight[:2], 16)
        # 将sim乘以255
        sim = int((1 - sim) * 255)
        # 计算lower的值，将color和weight的值分别减去sim
        lower = tuple(map(lambda c, w: max(0, c - w - sim), color, weight))
        # 计算upper的值，将color和weight的值分别加上sim，并取最小值255
        upper = tuple(map(lambda c, w: min(c + w + sim, 255), color, weight))
        return lower, upper

    @staticmethod
    def in_range(
        img: cv2.typing.MatLike, lower: Tuple[int, ...], upper: Tuple[int, ...]
    ) -> cv2.typing.MatLike:
        """
        将图像img中的像素值在lower和upper之间的部分提取出来，生成掩膜mask
        :param img: MatLike cv图像
        :param lower: 颜色范围的下限
        :param upper: 颜色范围的上限
        :return: MatLike 生成掩膜mask的cv图像
        """
        # 将图像img中的像素值在lower和upper之间的部分提取出来，生成掩膜mask
        mask = cv2.inRange(img, np.array(lower), np.array(upper))
        # 将原图像img和掩膜mask进行按位与操作，得到提取出来的部分
        img = cv2.bitwise_and(img, img, mask=mask)
        return img

    @staticmethod
    def ps_to_img(img: cv2.typing.MatLike, ps: str | Tuple) -> cv2.typing.MatLike:
        """
        :param img: cv图像
        :param ps: 偏色
        :return: 偏色后的cv图像
        """
        # 判断是RGB偏色还是HSV偏色,对应使用遮罩过滤
        if not ps:
            return img
        elif type(ps) == str:
            lower, upper = OpencvHelper.color_to_range(ps, 1)
            img = OpencvHelper.in_range(img, lower, upper)

        elif type(ps) == tuple or type(ps) == list:
            lower, upper = ps
            img_hsv1 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            img = OpencvHelper.in_range(img_hsv1, lower, upper)
            img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
        return img

    @staticmethod
    def lower_upper21(
        lower: Tuple[int, ...], upper: Tuple[int, ...]
    ) -> Tuple[list, list]:
        """
        颜色的上限和下限，-1或者+1，避免相等
        :param lower: 颜色的下限
        :param upper: 颜色的上限
        :return: 新的上限和下限
        """
        new_lower, new_upper = [], []
        for down, up in zip(lower, upper):
            if down == up > 0:
                down -= 1
            elif down == up == 0:
                up += 1
            new_lower.append(down)
            new_upper.append(up)
        return new_lower, new_upper

    @staticmethod
    def img_show(img: cv2.typing.MatLike) -> None:
        if img is None:
            raise "图像为空"
        windows_name = "img"
        cv2.imshow(windows_name, img)
        cv2.waitKey(0)
        # cv2.destroyWindow(windows_name)

    @staticmethod
    def find_pic_brisr(target_img, templ_img, delta_color):
        templImg = OpencvHelper.imread(templ_img)
        targetImg = OpencvHelper.imread(target_img)
        # BRISK 特征检测器
        # 判断是RGB偏色还是HSV偏色,对应使用遮罩过滤
        templImg = OpencvHelper.ps_to_img(templImg, delta_color)
        targetImg = OpencvHelper.ps_to_img(targetImg, delta_color)
        # 初始化BRISK特征检测器
        brisk = cv2.BRISK_create()
        # 在a和b中检测关键点和描述符
        kp1, des1 = brisk.detectAndCompute(templImg, None)
        kp2, des2 = brisk.detectAndCompute(targetImg, None)
        if des1 is None or des2 is None:
            print("特征找图失败")
            return None
        des1 = des1.astype("float32")
        des2 = des2.astype("float32")
        # 创建FLANN匹配器
        flann = cv2.FlannBasedMatcher()
        # 使用FLANN匹配器进行匹配
        matches = flann.knnMatch(des1, des2, k=2)

        # 定义比较函数
        def compare_ratio(match):
            # 返回第一个特征描述符距离与第二个特征描述符距离的比率
            return match[0].distance / match[1].distance

        # 进行排序
        matches = sorted(matches, key=compare_ratio)
        # 使用SANSAC过滤器进行匹配点过滤
        good_matches = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good_matches.append(m)

        img_matches = cv2.drawMatches(
            templImg,
            kp1,
            targetImg,
            kp2,
            good_matches,
            None,
            flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
        )
        if good_matches:
            return good_matches, kp1, img_matches

    @staticmethod
    def find_pic_bycv(target_img, templ_img, delta_color, sim, method):
        targetImg = OpencvHelper.imread(target_img)
        templImg = OpencvHelper.imread(templ_img)
        # 判断是RGB偏色还是HSV偏色,对应使用遮罩过滤
        # img1 = self.ps_to_img(img1, delta_color)
        # img2 = self.ps_to_img(img2, delta_color)
        # if gray:
        #     img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)  # 转灰度单通道
        #     img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)  # 转灰度单通道
        #     ret, img1 = cv2.threshold(img1, 0, 254, 0)  # 二值化
        #     ret, img2 = cv2.threshold(img2, 0, 254, 0)  # 二值化
        # result = cv2.matchTemplate(img1, img2, method)
        # 只匹配指定的颜色图像，参数mask表示参与匹配的像素矩阵
        if delta_color and isinstance(delta_color, str):
            # 将颜色转换为范围
            lower, upper = OpencvHelper.color_to_range(delta_color, 1.0)
            lower, upper = OpencvHelper.lower_upper21(lower, upper)
            mask = cv2.inRange(templImg, tuple(lower), tuple(upper))
        elif delta_color and (
            isinstance(delta_color, list) or isinstance(delta_color, tuple)
        ):
            lower, upper = delta_color
            # lower, upper = lower_upper21(lower, upper)
            img2_hsv = cv2.cvtColor(templImg, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(img2_hsv, tuple(lower), tuple(upper))
        else:
            mask = None
        # 进行模板匹配
        result = cv2.matchTemplate(targetImg, templImg, method, mask=mask)
        # 获取匹配结果
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        yloc, xloc = np.where(result >= sim)
        height, width = templImg.shape[:2]
        return result, min_val, max_val, min_loc, max_loc, yloc, xloc, height, width

    # 单点比色
    @staticmethod
    def cmp_color(img, x, y, color, sim=1):
        """
        :param x: 坐标x
        :param y: 坐标y
        :param color: 颜色字符串,可以支持偏色,"ffffff-202020",最多支持一个
        :param sim:相似度(0.1-1.0) (0,255)
        :return:bool
        """
        lower, upper = OpencvHelper.color_to_range(color, sim)
        if not lower is None:
            new_color = img[y, x]
            for i in [0, 1, 2]:
                if new_color[i] < lower[i] or new_color[i] > upper[i]:
                    return False
            return True
        return False

    # 范围找色
    @staticmethod
    def find_range_color(img, color, sim):
        lower, upper = OpencvHelper.color_to_range(color, sim)
        img_array = np.array(img)
        mask1 = np.all(img_array >= lower, axis=-1)
        mask2 = np.all(img_array <= upper, axis=-1)
        mask = np.logical_and(mask1, mask2)
        pos = np.argwhere(mask)
        if len(pos):
            y, x = pos[0]
            return x, y

    # 特征找图
    @staticmethod
    def find_pic_bytz(
        target_img=None,
        templ_img=None,
        delta_color="",
        drag=None,
    ):
        resoult = OpencvHelper.find_pic_brisr(target_img, templ_img, delta_color)

        if resoult:
            good_matches, kp1, img = resoult
            m = good_matches[0]
            if drag:
                OpencvHelper.img_show(img)
            # 浮点数转整数
            pts1 = np.array(kp1[m.queryIdx].pt, dtype=np.float32).astype(np.int32)
            return list(pts1)

    # cv找图
    @staticmethod
    def find_pic(
        target_img=None,
        templ_img=None,
        delta_color="",
        sim=0.9,
        method=5,
        drag=None,
        center=None,
    ):
        """
        :param target_img:目标cv图片
        :param templ_img:找图的cv小图片
        :param delta_color:偏色,可以是RGB偏色,格式"FFFFFF-202020",也可以是HSV偏色，格式((0,0,0),(180,255,255))
        :param sim:相似度，和算法相关
        :param method:仿大漠，总共有5总，范围0-5,对应cv的算法
               方差匹配方法：匹配度越高，值越接近于0。
               归一化方差匹配方法：完全匹配结果为0。
               相关性匹配方法：完全匹配会得到很大值，不匹配会得到一个很小值或0。
               归一化的互相关匹配方法：完全匹配会得到1， 完全不匹配会得到0。
               相关系数匹配方法：完全匹配会得到一个很大值，完全不匹配会得到0，完全负相关会得到很大的负数。
                    （此处与书籍以及大部分分享的资料所认为不同，研究公式发现，只有归一化的相关系数才会有[-1,1]的值域）
               归一化的相关系数匹配方法：完全匹配会得到1，完全负相关匹配会得到-1，完全不匹配会得到0。
        :param drag:是否在找到的位置画图并显示,默认不画
        :param center:获取结果的中心点
        :return:x,y
        """
        targetImg = OpencvHelper.imread(target_img)
        resoult = OpencvHelper.find_pic_bycv(
            targetImg,
            templ_img,
            delta_color,
            sim,
            method,
        )
        result, min_val, max_val, min_loc, max_loc, yloc, xloc, height, width = resoult
        # 画图
        if len(xloc):
            x, y = max_loc[0], max_loc[1]
            if center:  # 获取中心位置
                x = x + width // 2
                y = y + height // 2
                width = 2
                height = 2
            if drag:
                img = cv2.rectangle(
                    targetImg,
                    (x, y),
                    (x + width, y + height),
                    (255, 0, 0),
                    thickness=2,
                )
                OpencvHelper.img_show(img)
            return x, y

    @staticmethod
    def imread(path):
        if type(path) == str:
            if not os.path.exists(path):
                raise f"图片路径不存在{path}"
            # 读取图片
            if OpencvHelper.is_chinese(path):
                img = cv2.imdecode(
                    np.fromfile(path, dtype=np.uint8), 1
                )  # 避免路径有中文
            else:
                img = cv2.imread(path)
            return img
        return path

    @staticmethod
    def is_chinese(string):
        """
        检查整个字符串是否包含中文
        :param string: 需要检查的字符串
        :return: bool
        """
        for ch in string:
            if "\u4e00" <= ch <= "\u9fff":
                return True
        return False
