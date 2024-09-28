"""
標準地域メッシュの処理

ref: https://www.stat.go.jp/data/mesh/pdf/gaiyo1.pdf (p.8)
"""
import re
from typing import Tuple


def get_extent(code: str) -> Tuple[float, float, float, float]:
    """
    メッシュコード長からメッシュレベルを判定して経緯度範囲を取得する。
    """
    code = re.sub(r'\D', '', code)
    code_len = len(code)
    if code_len == 4:
        return get_level1_extent(code)
    if code_len == 6:
        return get_level2_extent(code)
    if code_len == 7:
        return get_2km_extent(code)
    if code_len == 8:
        return get_level3_extent(code)
    if code_len == 9:
        if code[8] == "5":
            return get_5km_extent(code)
        if code[8] in "1234":
            return get_level4_extent(code)
        else:
            raise ValueError(f"Code '{code}' is invalid.")
    if code_len == 10:
        return get_level5_extent(code)
    if code_len == 11:
        return get_level6_extent(code)

    raise ValueError(f"Code '{code}' is invalid.")


def get_level1_extent(code: str) -> Tuple[float, float, float, float]:
    """
    1次メッシュコードから経緯度範囲を取得する。
    """
    code = re.sub(r'\D', '', code)
    if len(code) != 4:
        raise ValueError(f"Code '{code}' is invalid for level1 mesh.")

    lat0 = float(code[0:2]) / 1.5
    lon0 = float(code[2:4]) + 100
    lat1 = lat0 + 2.0 / 3.0
    lon1 = lon0 + 1.0
    return (lon0, lat0, lon1, lat1)


def get_level2_extent(code: str) -> Tuple[float, float, float, float]:
    """
    2次メッシュコードから経緯度範囲を取得する。
    """
    code = re.sub(r'\D', '', code)
    if len(code) != 6:
        raise ValueError(f"Code '{code}' is invalid for level2 mesh.")

    lat0 = float(code[0:2]) / 1.5 + float(code[4]) / 12.0
    lon0 = float(code[2:4]) + 100 + float(code[5]) / 8.0
    lat1 = lat0 + 1.0 / 12.0
    lon1 = lon0 + 1.0 / 8.0
    return (lon0, lat0, lon1, lat1)


def get_level3_extent(code: str) -> Tuple[float, float, float, float]:
    """
    3次メッシュコードから経緯度範囲を取得する。
    """
    code = re.sub(r'\D', '', code)
    if len(code) != 8:
        raise ValueError(f"Code '{code}' is invalid for level3 mesh.")

    lat0 = float(code[0:2]) / 1.5 + float(code[4]) / \
        12.0 + float(code[6]) / 120.0
    lon0 = float(code[2:4]) + 100 + float(code[5]) / \
        8.0 + float(code[7]) / 80.0
    lat1 = lat0 + 1.0 / 120.0
    lon1 = lon0 + 1.0 / 80.0
    return (lon0, lat0, lon1, lat1)


def get_level4_extent(code: str) -> Tuple[float, float, float, float]:
    """
    2分の1地域メッシュコードから経緯度範囲を取得する。
    """
    code = re.sub(r'\D', '', code)
    if len(code) != 9 or code[8] not in "1234":
        raise ValueError(f"Code '{code}' is invalid for level4 mesh.")

    lat0 = float(code[0:2]) / 1.5 + float(code[4]) / 12.0 \
        + float(code[6]) / 120.0 \
        + float(1.0 / 240.0) * int(code[8] in "34")
    lon0 = float(code[2:4]) + 100 + float(code[5]) / 8.0 \
        + float(code[7]) / 80.0 \
        + float(1.0 / 160.0) * int(code[8] in "24")
    lat1 = lat0 + 1.0 / 240.0
    lon1 = lon0 + 1.0 / 160.0
    return (lon0, lat0, lon1, lat1)


def get_level5_extent(code: str) -> Tuple[float, float, float, float]:
    """
    4分の1地域メッシュコードから経緯度範囲を取得する。
    """
    code = re.sub(r'\D', '', code)
    if len(code) != 10 or code[8] not in "1234" \
            or code[9] not in "1234":
        raise ValueError(f"Code '{code}' is invalid for level5 mesh.")

    lat0 = float(code[0:2]) / 1.5 + float(code[4]) / 12.0 \
        + float(code[6]) / 120.0 \
        + float(1.0 / 240.0) * int(code[8] in "34") \
        + float(1.0 / 480.0) * int(code[9] in "34")
    lon0 = float(code[2:4]) + 100 + float(code[5]) / 8.0 \
        + float(code[7]) / 80.0 \
        + float(1.0 / 160.0) * int(code[8] in "24") \
        + float(1.0 / 320.0) * int(code[9] in "24")
    lat1 = lat0 + 1.0 / 480.0
    lon1 = lon0 + 1.0 / 320.0
    return (lon0, lat0, lon1, lat1)


def get_level6_extent(code: str) -> Tuple[float, float, float, float]:
    """
    8分の1地域メッシュコードから経緯度範囲を取得する。
    """
    code = re.sub(r'\D', '', code)
    if len(code) != 11 or code[8] not in "1234" \
            or code[9] not in "1234" or code[10] not in "1234":
        raise ValueError(f"Code '{code}' is invalid for level6 mesh.")

    lat0 = float(code[0:2]) / 1.5 + float(code[4]) / 12.0 \
        + float(code[6]) / 120.0 \
        + float(1.0 / 240.0) * int(code[8] in "34") \
        + float(1.0 / 480.0) * int(code[9] in "34") \
        + float(1.0 / 960.0) * int(code[10] in "34")
    lon0 = float(code[2:4]) + 100 + float(code[5]) / 8.0 \
        + float(code[7]) / 80.0 \
        + float(1.0 / 160.0) * int(code[8] in "24") \
        + float(1.0 / 320.0) * int(code[9] in "24") \
        + float(1.0 / 640.0) * int(code[10] in "24")
    lat1 = lat0 + 1.0 / 960.0
    lon1 = lon0 + 1.0 / 640.0
    return (lon0, lat0, lon1, lat1)


def get_2km_extent(code: str) -> Tuple[float, float, float, float]:
    """
    統合2倍地域メッシュコードから経緯度範囲を取得する。
    """
    code = re.sub(r'\D', '', code)
    if len(code) != 9 or code[8] != "5":
        raise ValueError(f"Code '{code}' is invalid for 2km mesh.")

    lat0 = float(code[0:2]) / 1.5 + float(code[4]) / 12.0 \
        + float(code[6]) / 120.0
    lon0 = float(code[2:4]) + 100 + float(code[5]) / 8.0 \
        + float(code[7]) / 80.0
    lat1 = lat0 + 1.0 / 60.0
    lon1 = lon0 + 1.0 / 40.0
    return (lon0, lat0, lon1, lat1)


def get_5km_extent(code: str) -> Tuple[float, float, float, float]:
    """
    統合5倍地域メッシュコードから経緯度範囲を取得する。
    """
    code = re.sub(r'\D', '', code)
    if len(code) != 7 or code[6] not in "1234":
        raise ValueError(f"Code '{code}' is invalid for 5km mesh.")

    lat0 = float(code[0:2]) / 1.5 + float(code[4]) / 12.0 \
        + float(code[6] in "34") / 24.0
    lon0 = float(code[2:4]) + 100 + float(code[5]) / 8.0 \
        + float(code[6] in "24") / 16.0
    lat1 = lat0 + 1.0 / 24.0
    lon1 = lon0 + 1.0 / 16.0
    return (lon0, lat0, lon1, lat1)


def get_level1_meshcode(lon: float, lat: float) -> str:
    """
    経緯度から1次メッシュコード (4文字) を取得する。
    """
    return get_level6_meshcode(lon, lat)[0:4]


def get_level2_meshcode(lon: float, lat: float) -> str:
    """
    経緯度から2次メッシュコード (6文字) を取得する。
    """
    return get_level6_meshcode(lon, lat)[0:6]


def get_level3_meshcode(lon: float, lat: float) -> str:
    """
    経緯度から3次メッシュコード (8文字) を取得する。
    """
    return get_level6_meshcode(lon, lat)[0:8]


def get_level4_meshcode(lon: float, lat: float) -> str:
    """
    経緯度から2分の1地域メッシュコード (9文字) を取得する。
    """
    return get_level6_meshcode(lon, lat)[0:9]


def get_level5_meshcode(lon: float, lat: float) -> str:
    """
    経緯度から4分の1地域メッシュコード (10文字) を取得する。
    """
    return get_level6_meshcode(lon, lat)[0:10]


def get_level6_meshcode(lon: float, lat: float) -> str:
    """
    経緯度から8分の1地域メッシュコード (11文字) を取得する。
    """
    # 1次メッシュコード
    y, x = lat * 1.5, lon - 100.0
    d0, d1 = int(y), int(x)
    modx, mody = x - d1, y - d0

    # 2次メッシュコード (8x8 分割)
    x, y = modx * 8.0, mody * 8.0
    d2, d3 = int(y), int(x)
    modx, mody = x - d3, y - d2

    # 3次メッシュコード (10x10 分割)
    x, y = modx * 10.0, mody * 10.0
    d4, d5 = int(y), int(x)
    modx, mody = x - d5, y - d4

    # 4次 (1/2) メッシュコード (2x2 分割)
    x, y = modx * 2.0, mody * 2.0
    d6 = 1 + 2 * int(y >= 1.0) + int(x >= 1.0)
    modx, mody = x - float(d6 in (2, 4)), y - float(d6 in (3, 4))

    # 5次 (1/4) メッシュコード (2x2 分割)
    x, y = modx * 2.0, mody * 2.0
    d7 = 1 + 2 * int(y >= 1.0) + int(x >= 1.0)
    modx, mody = x - float(d7 in (2, 4)), y - float(d7 in (3, 4))

    # 6次 (1/8) メッシュコード (2x2 分割)
    x, y = modx * 2.0, mody * 2.0
    d8 = 1 + 2 * int(y >= 1.0) + int(x >= 1.0)

    return "{:02d}{:02d}{:01d}{:01d}{:01d}{:01d}{:01d}{:01d}{:01d}".format(
        d0, d1, d2, d3, d4, d5, d6, d7, d8
    )


def get_2km_meshcode(lon: float, lat: float) -> str:
    """
    経緯度から統合2倍地域メッシュコード (9文字) を取得する。
    """
    code = get_level6_meshcode(lon, lat)
    c6 = chr(ord(code[6]) - 1) if code[6] in "13579" else code[6]
    c7 = chr(ord(code[7]) - 1) if code[7] in "13579" else code[7]
    return code[0:6] + c6 + c7 + "5"


def get_5km_meshcode(lon: float, lat: float) -> str:
    """
    経緯度から統合5倍地域メッシュコード (7文字) を取得する。
    """
    code = get_level6_meshcode(lon, lat)
    d6 = 1 + 2 * int(code[6] >= "5") + int(code[7] >= "5")

    return code[0:6] + "{:01d}".format(d6)


if __name__ == "__main__":

    tests = [
        ("札幌市役所",   43.06197357, 141.35437012,
         "6441-4278-143", "6441-4268-5", "6441-424"),
        ("新宿区役所",   35.69388962, 139.70346069,
         "5339-4536-141", "5339-4526-5", "5339-452"),
        ("明石市役所",   34.64310837, 134.99717712,
         "5134-7779-223", "5134-7768-5", "5134-774"),
        ("宮古島市役所", 24.80549049, 125.28115845,
         "3725-1262-324", "3725-1262-5", "3725-123"),
    ]

    for t in tests:
        # 1/8 メッシュコードが一致することを確認
        answer = re.sub(r'\D', '', t[3])
        code = get_level6_meshcode(lon=t[2], lat=t[1])
        assert (code == answer)

        # 2倍メッシュコードが一致することを確認
        answer = re.sub(r'\D', '', t[4])
        code = get_2km_meshcode(lon=t[2], lat=t[1])
        assert (code == answer)

        # 5倍メッシュコードが一致することを確認
        answer = re.sub(r'\D', '', t[5])
        code = get_5km_meshcode(lon=t[2], lat=t[1])
        assert (code == answer)

        # メッシュコードがあらわす範囲に含まれることを確認
        code = get_level6_meshcode(lon=t[2], lat=t[1])

        extent = get_extent(code[0:4])
        assert (
            extent[1] <= t[1] and extent[3] > t[1]
            and extent[0] <= t[2] and extent[2] > t[2]
        )
        assert (extent[2] - extent[0] == 1.0)

        extent = get_extent(code[0:6])
        assert (
            extent[1] <= t[1] and extent[3] > t[1]
            and extent[0] <= t[2] and extent[2] > t[2]
        )
        assert (abs(1 - (extent[2] - extent[0]) * 8) < 1.0e-10)

        extent = get_extent(code[0:8])
        assert (
            extent[1] <= t[1] and extent[3] > t[1]
            and extent[0] <= t[2] and extent[2] > t[2]
        )
        assert (abs(1 - (extent[2] - extent[0]) * 80) < 1.0e-10)

        extent = get_extent(code[0:9])
        assert (
            extent[1] <= t[1] and extent[3] > t[1]
            and extent[0] <= t[2] and extent[2] > t[2]
        )
        assert (abs(1 - (extent[2] - extent[0]) * 160) < 1.0e-10)

        extent = get_extent(code[0:10])
        assert (
            extent[1] <= t[1] and extent[3] > t[1]
            and extent[0] <= t[2] and extent[2] > t[2]
        )
        assert (abs(1 - (extent[2] - extent[0]) * 320) < 1.0e-10)

        extent = get_extent(code[0:11])
        assert (
            extent[1] <= t[1] and extent[3] > t[1]
            and extent[0] <= t[2] and extent[2] > t[2]
        )
        assert (abs(1 - (extent[2] - extent[0]) * 640) < 1.0e-10)
