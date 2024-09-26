import json
import time


def to_int(obj):
    try:
        return int(obj)
    except Exception:
        return 0


def to_float(obj):
    try:
        return float(obj)
    except Exception:
        return 0.0


def null_to_str_null(obj):
    if obj is None or obj == "":
        return "null"
    else:
        return obj


def null_to_empty(obj):
    if obj is None or obj is False:
        return ""
    else:
        return obj


def null_to_zero(obj):
    if obj is None or obj is False:
        return 0
    else:
        return obj


def null_to_str(obj):
    if obj is None or obj is False:
        return ""
    else:
        return obj


def null_to_str_zero(obj):
    if obj is None or obj is False:
        return "0"
    else:
        return obj


def get_json_text(content):
    if not content:
        return ""
    try:
        s_json = json.loads(content)
        return "".join([item["text"] for item in s_json if item["type"] == 1])
    except Exception:
        return content


def ts2dt(ts):
    """
    时间戳转时间
    :param ts: 1519960417
    :return: datetime str
    """
    if len(str(int(ts))) == 13:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts / 1000))
    else:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))


def str2json(content):
    if not content:
        return ""
    try:
        return json.loads(content)
    except Exception:
        return content


def transfer_url(pic_id):
    try:
        if not pic_id:
            return ""

        if pic_id.startswith("http"):
            return pic_id

        img_exts = ["jpg", "gif", "bmp", "jpeg", "png"]
        if "_" not in pic_id or "." not in pic_id:
            return ""

        split_res = pic_id.split("_")
        if not split_res:
            return ""
        id_ext = split_res[0]
        id_ext_arr = id_ext.split(".")
        if len(id_ext_arr) < 2:
            return ""
        _id = id_ext_arr[0]
        ext_s = id_ext_arr[1]
        id_dir = str(int(_id) + 100000000)
        dir = id_dir[0:3] + "/" + id_dir[3:6] if len(id_dir) > 6 else ""

        ext_index = int(ext_s) - 1
        ext = img_exts[ext_index] if 0 < ext_index < len(img_exts) else None

        if dir and ext:
            last = int(_id[-1:])
            i = "" if last <= 3 else ("2" if last <= 5 else "3")
            return "http://tgi1" + i + ".jia.com/" + dir + "/" + _id + "." + ext

        return ""
    except Exception:
        return ""
