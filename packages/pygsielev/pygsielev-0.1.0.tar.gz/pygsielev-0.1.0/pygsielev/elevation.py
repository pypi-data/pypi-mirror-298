import glob
import io
import math
import os
from pathlib import Path
import re
from typing import Optional, Tuple
import zipfile

from pygsielev.standard_meshcode import get_level3_meshcode


class ElevationExtractor(object):

    re_mesh = re.compile(r"<mesh>(\d+)</mesh>")
    re_lower = re.compile(
        r"<gml:lowerCorner>([\d\.]+)\s+([\d\.]+)</gml:lowerCorner>")
    re_upper = re.compile(
        r"<gml:upperCorner>([\d\.]+)\s+([\d\.]+)</gml:upperCorner>")
    re_high = re.compile(r"<gml:high>(\d+)\s+(\d+)</gml:high>")
    re_data_start = re.compile(r"<gml:tupleList>")
    re_data_end = re.compile(r"</gml:tupleList>")
    re_startpoint = re.compile(
        r"<gml:startPoint>([\d\.].+)\s+([\d\.]+)</gml:startPoint>")

    def __init__(self, data_dir: Optional[os.PathLike] = None):
        self.data_dir = data_dir or os.environ.get("GSIELEV_DATADIR")
        if self.data_dir is None:
            raise RuntimeError((
                "Please set the data directory with a parameter or "
                "the environmental variable GSIELEV_DATADIR."
            ))
        self.data_dir = Path(self.data_dir)
        self.clear()

    def clear(self):
        self.mesh = None
        self.start_pos = 0
        self.data = None
        self.extent = None
        self.gridsize = None

    def get_elevation(self, lon: float, lat: float) -> Tuple[float, str]:
        if self.extent is None or \
                lon < self.extent[0] or lat < self.extent[1] or \
                lon >= self.extent[2] or lat >= self.extent[3]:

            meshcode = get_level3_meshcode(lon=lon, lat=lat)
            self.read_xml_file(meshcode)

        if self.mesh is None:
            return (math.nan, 'データなし')

        xpos = int(self.gridsize[0] * (
            lon - self.extent[0]) /
            (self.extent[2] - self.extent[0])
        )
        ypos = int(self.gridsize[1] * (
            1.0 - (lat - self.extent[1]) /
            (self.extent[3] - self.extent[1])
        ))
        pos = ypos * self.gridsize[0] + xpos - self.start_pos
        if pos < 0 or pos >= len(self.data):
            return (math.nan, 'データなし')

        return self.data[pos]

    def read_xml_file(self, meshcode: str) -> None:
        level2code = meshcode[0:4] + '-' + meshcode[4:6]
        zipfiles = glob.glob(
            str(self.data_dir / f"FG-GML-{level2code}-DEM*.zip"))
        if len(zipfiles) == 0:
            raise RuntimeError((
                f"Zip file for code:'{level2code}' is not available yet. "
                "Please download it and place in the 'data/' directory."
            ))

        level3code = meshcode[0:4] + '-' + meshcode[4:6] + '-' + meshcode[6:8]
        re_target = re.compile(rf".*FG-GML-{level3code}-.*.xml")

        with zipfile.ZipFile(zipfiles[0], "r") as zipf:
            for filename in zipf.namelist():
                m = re_target.match(filename)
                if m is not None:
                    xmlfile = filename
                    break

            else:
                self.clear()
                return

            with zipf.open(xmlfile, "r") as binf:
                f = io.TextIOWrapper(binf, encoding="utf-8")

                # Get meshcode
                for ln in f:
                    m = self.__class__.re_mesh.search(ln)
                    if m != None:
                        self.mesh = m.group(1)
                        break

                # Get lower and upper coordinates
                for ln in f:
                    m = self.__class__.re_lower.search(ln)
                    if m != None:
                        lower_coords = (float(m.group(2)), float(m.group(1)))
                        break

                for ln in f:
                    m = self.__class__.re_upper.search(ln)
                    if m != None:
                        upper_coords = (float(m.group(2)), float(m.group(1)))
                        break

                self.extent = (lower_coords[0], lower_coords[1],
                               upper_coords[0], upper_coords[1])

                # Get grid size
                for ln in f:
                    m = self.__class__.re_high.search(ln)
                    if m != None:
                        xlen = int(m.group(1)) + 1
                        ylen = int(m.group(2)) + 1
                        self.gridsize = (xlen, ylen)
                        break

                # Seek data head
                for ln in f:
                    m = self.__class__.re_data_start.search(ln)
                    if m != None:
                        break

                # data
                data = []
                r = re.compile("</gml:tupleList>")
                for ln in f:
                    m = self.__class__.re_data_end.search(ln)
                    if m != None:
                        break
                    else:
                        vars = ln.strip().split(',')
                        loctype, value = vars[0], float(vars[1])
                        if value < -9000:
                            data.append((math.nan, loctype))
                        else:
                            data.append((value, loctype))

                # start point
                startx = starty = 0
                for ln in f:
                    m = self.__class__.re_startpoint.search(ln)
                    if m != None:
                        startx = int(m.group(1))
                        starty = int(m.group(2))
                        break

        # data2 = np.full(xlen * ylen, np.nan)
        self.start_pos = starty * xlen + startx
        self.data = data

    def write_text_dem(self, fname: os.PathLike):
        with open(fname, "w") as tmpf:
            for y in range(self.gridsize[1]):
                if y % 10 == 0:
                    for x in range(self.gridsize[0]):
                        if x % 10 == 0:
                            print("| ", end='', file=tmpf)

                        print("------ ", end='', file=tmpf)

                    print("", file=tmpf)

                for x in range(self.gridsize[0]):
                    if x % 10 == 0:
                        print("| ", end='', file=tmpf)

                    pos = y * self.gridsize[0] + x - self.start_pos
                    if pos < 0:
                        print("     * ", end='', file=tmpf)

                    else:
                        print("{:6.1f} ".format(
                            self.data[pos][0]), end='', file=tmpf)

                print("", file=tmpf)


if __name__ == "__main__":
    engine = ElevationExtractor()
    # https://maps.gsi.go.jp/#17/35.288180/139.573510/&base=std&ls=std&disp=1&vs=c1g1j0h0k0l0u0t0z0r0s0m0f1
    print(engine.get_elevation(
        lon=139.573510,
        lat=35.288180,
    ))

    # https://maps.gsi.go.jp/#17/35.287474/139.582647/&base=std&ls=std&disp=1&vs=c1g1j0h0k0l0u0t0z0r0s0m0f1
    print(engine.get_elevation(
        lon=139.582647,
        lat=35.287474,
    ))
    # https://maps.gsi.go.jp/#18/35.286960/139.584532/&base=std&ls=std&disp=1&vs=c1g1j0h0k0l0u0t0z0r0s0m0f1
    print(engine.get_elevation(
        lon=139.584532,
        lat=35.286960,
    ))
