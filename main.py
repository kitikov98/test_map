from rosreestr2coord import Area
import json
from pyproj import Proj, Transformer


# 24:39:101001:369
print('Введите кадастровый номер: ')
cadastr = input()
area = Area(cadastr)
# аргументы
#   code='' - кадастровый номер участка
#   area_type=1 - тип площади
#   epsilon=5 - точность аппроксимации
#   media_path='' - путь для временных файлов
#   with_log=True - логирование
#   coord_out='EPSG:4326' - или EPSG:3857 (будет удалена в последующих версиях)
#   center_only=False - экспорт координат центров участка
#   with_proxy=False - запросы через прокси
#   use_cache=True - использовать кэширование запросов
area.to_geojson()
area.to_geojson_poly()
area.get_coord()  # [[[area1_xy], [hole1_xy], [hole2_xy]], [[area2_xyl]]]
area.get_attrs()

name_cadastr = cadastr.replace(':', '_')

way = 'tmp/' + name_cadastr + '/feature_info.json'
jsonway = 'tmp/' + name_cadastr + '/data.json'

with open(way, 'r', encoding='utf-8') as f:
    text = json.load(f)
    xmax = text['feature']['extent']['xmax']
    ymax = text['feature']['extent']['ymax']
    xmin = text['feature']['extent']['xmin']
    ymin = text['feature']['extent']['ymin']
    # xcenter = text['feature']['center']['x']
    # ycenter = text['feature']['center']['y']
    # print(xmax, ymax, xmin, ymin, xcenter, ycenter)

proj = Transformer.from_crs(3857, 4326, always_xy=True)
x1, y1 = proj.transform(xmax, ymax)
x2, y2 = proj.transform(xmin, ymin)


dict = {"type": "FeatureCollection",
        "metadata": {"name": "24:39:101001:369", "creator": "Yandex Map Constructor"},
        "features": [{"properties": {"fill": "#ff5c5c", "stroke": "#ff5c5c"},
                      "type": "Feature",
                      "id": "0",
                      "geometry": {"type": "Polygon",
                                   "coordinates": [[[x1, y1], [x2, y1],
                                                    [x2, y2], [x1, y2],
                                                    [x1, y1]]]}
                      }
                     ]
        }


with open(jsonway, 'w') as f:
    json.dump(dict, f)

