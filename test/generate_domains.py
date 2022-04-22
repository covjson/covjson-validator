from collections import namedtuple
import json
from pathlib import Path
import shutil
import exhaust

from .compact_json import CompactJSONEncoder

Spec = namedtuple('Spec', ['x', 'y', 'z', 't', 'composite'])
C = namedtuple('Composite', ['cardinality', 'data_type', 'coordinates'])
DOMAIN_TYPES = {
    'Grid':               Spec('+', '+', '[+]', '[+]', ''),
    'VerticalProfile':    Spec('1', '1',  '+',  '[1]', ''),
    'PointSeries':        Spec('1', '1', '[1]',  '+',  ''),
    'Point':              Spec('1', '1', '[1]', '[1]', ''),
    'MultiPointSeries':   Spec('',  '',  '',     '+',  C('+', 'tuple', ['xyz', 'xy'])),
    'MultiPoint':         Spec('',  '',  '',    '[1]', C('+', 'tuple', ['xyz', 'xy'])),
    'PolygonSeries':      Spec('',  '',  '[1]',  '+',  C('1', 'polygon', ['xy'])),
    'Polygon':            Spec('',  '',  '[1]', '[1]', C('1', 'polygon', ['xy'])),
    'MultiPolygonSeries': Spec('',  '',  '[1]',  '+',  C('+', 'polygon', ['xy'])),
    'MultiPolygon':       Spec('',  '',  '[1]', '[1]', C('+', 'polygon', ['xy'])),
    'Trajectory':         Spec('',  '',  '[1]',  '',   C('+', 'tuple', ['txyz', 'txy'])),
    'Section':            Spec('',  '',   '+',   '',   C('+', 'tuple', ['txy'])),
}


def generate_domains_of_type(domain_type):
    yield from exhaust.space(
            lambda space: get_domain_of_type(domain_type, space))


def get_domain_of_type(domain_type, state):
    ''' Returns a random domain of the specified domain type '''

    labels = []

    time_values = ["2008-01-01T04:00:00Z",
                   "2008-01-01T05:00:00Z",
                   "2008-01-01T06:00:00Z"]
    numeric_values = [1, 2, 3]

    time_axis_single = {
        "values": [time_values[0]]
    }
    time_axis_multi = {
        "values": time_values
    }
    numeric_axis_single = {
        "values": [numeric_values[0]]
    }
    numeric_axis_multi = {
        "values": numeric_values
    }
    numeric_axis_regular = {
        "start": 20, "stop": 40, "num": 100
    }

    label_missing = '0'
    label_single = '1'
    label_numeric_multi = f'{len(numeric_values)}'
    label_time_multi = f'{len(time_values)}'
    label_numeric_regular = 'reg'

    spec = DOMAIN_TYPES[domain_type]._asdict()
    axes = {}
    for name, info in spec.items():
        if info == '':
            continue
        if name in ['x', 'y', 'z', 't']:
            cardinality = info
            if name == 't':
                axis_single = time_axis_single
                axis_multi = time_axis_multi
                label_multi = label_time_multi
            elif name in ['x', 'y']:
                axis_single = numeric_axis_single
                axis_multi = numeric_axis_regular
                label_multi = label_numeric_regular
            elif name == 'z':
                axis_single = numeric_axis_single
                axis_multi = numeric_axis_multi
                label_multi = label_numeric_multi
            else:
                assert False, "Invalid axis name"

            if cardinality == '1':
                axes[name] = axis_single
            elif cardinality == '+':
                if state.maybe():
                    axes[name] = axis_single
                    labels.append(f"{name}={label_single}")
                else:
                    axes[name] = axis_multi
                    labels.append(f"{name}={label_multi}")
            elif cardinality == '[1]':
                if state.maybe():
                    axes[name] = axis_single
                    labels.append(f"{name}={label_single}")
                else:
                    labels.append(f"{name}={label_missing}")
            elif cardinality == '[+]':
                if state.maybe():
                    if state.maybe():
                        axes[name] = axis_single
                        labels.append(f"{name}={label_single}")
                    else:
                        axes[name] = axis_multi
                        labels.append(f"{name}={label_multi}")
                else:
                    labels.append(f"{name}={label_missing}")
            else:
                assert False, "Invalid axis cardinality"
        elif name == 'composite':
            existing_axes = list(axes.keys())
            possible_coordinates = [
                c for c in info.coordinates
                if set(c) & set(existing_axes) == set()
            ]
            coordinates = list(state.choice(possible_coordinates))
            if len(info.coordinates) > 1:
                labels.append(f"cc={''.join(coordinates)}")
            if info.data_type == 'tuple':
                vals_by_axis = dict(
                    t=time_values,
                    x=numeric_values,
                    y=numeric_values,
                    z=numeric_values
                )
                values = [list(item) for item in
                          zip(*[vals_by_axis[c] for c in coordinates])]
            elif info.data_type == 'polygon':
                values = [
                    [ [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0] ]  ],
                    [ [ [200.0, 10.0], [201.0, 10.0], [201.0, 11.0], [200.0, 11.0], [200.0, 10.0] ] ]
                ]
            else:
                assert False, "Invalid composite data type"

            if info.cardinality == '1':
                values = [values[0]]
            elif info.cardinality == '+':
                count = state.choice([1, len(values)])
                values = values[:count]
                labels.append(f"c={count}")
            else:
                assert False, "Invalid composite cardinality"

            axes[name] = {
                "dataType": info.data_type,
                "coordinates": coordinates,
                "values": values
            }
        else:
            assert False, "Invalid axis name"

    coordinates = []
    for name, info in axes.items():
        if name in ['x', 'y', 'z', 't']:
            coordinates.append(name)
        elif name == 'composite':
            coordinates += info['coordinates']
        else:
            assert False, "Invalid axis name"

    referencing = []
    if 't' in coordinates:
        coordinates.remove('t')
        referencing.append({
            "coordinates": ["t"],
            "system": {
                "type": "TemporalRS",
                "calendar": "Gregorian"
            }
        })
    if 'x' in coordinates and 'y' in coordinates:
        coordinates.remove('x')
        coordinates.remove('y')
        referencing.append({
            "coordinates": ["x", "y"],
            "system": {
                "type": "GeographicCRS",
                "id": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
            }
        })
    if 'z' in coordinates:
        coordinates.remove('z')
        referencing.append({
            "coordinates": ["z"],
            "system": {
                "type": "VerticalCRS",
                "id": "http://www.opengis.net/def/crs/EPSG/0/5703"
            }
        })

    assert not coordinates, f"Unexpected coordinates: {coordinates}"

    domain = {
        "type": "Domain",
        "domainType": domain_type,
        "axes": axes,
        "referencing": referencing
    }

    label = ','.join(labels)

    return domain, label


if __name__ == "__main__":
    this_dir = Path(__file__).parent
    domain_dir = this_dir / 'test_data' / 'domains'
    domain_dir.mkdir(parents=True, exist_ok=True)

    for domain_type in DOMAIN_TYPES.keys():
        domain_type_dir = domain_dir / domain_type
        if domain_type_dir.exists():
            shutil.rmtree(domain_type_dir)
        domain_type_dir.mkdir()
        jsons = []
        paths = []
        for domain, label in generate_domains_of_type(domain_type):
            path = domain_type_dir / f'{domain_type}_{label}.json'
            paths.append(path)
            with path.open('w') as f:
                j = json.dumps(domain, indent=2, cls=CompactJSONEncoder)
                f.write(j)
                jsons.append(j)
        assert len(set(jsons)) == len(jsons), "Duplicate domains generated"
        assert len(set(paths)) == len(paths), "Duplicate notes generated"
