from collections import namedtuple
import random

Spec = namedtuple('Spec', ['x', 'y', 'z', 't', 'composite'])
C = namedtuple('Composite', ['cardinality', 'data_type', 'coordinates'])
DOMAIN_TYPES = {
    'Grid':               Spec('+', '+', '[+]', '[+]', ''),
    # 'VerticalProfile':    Spec('1', '1',  '+',  '[1]', ''),
    # 'PointSeries':        Spec('1', '1', '[1]',  '+',  ''),
    # 'Point':              Spec('1', '1', '[1]', '[1]', ''),
    # 'MultiPointSeries':   Spec('',  '',  '',     '+',  C('+', 'tuple', ['xyz', 'xy'])),
    # 'MultiPoint':         Spec('',  '',  '',    '[1]', C('+', 'tuple', ['xyz', 'xy'])),
    # 'PolygonSeries':      Spec('',  '',  '[1]',  '+',  C('1', 'polygon', ['xy'])),
    # 'Polygon':            Spec('',  '',  '[1]', '[1]', C('1', 'polygon', ['xy'])),
    # 'MultiPolygonSeries': Spec('',  '',  '[1]',  '+',  C('+', 'polygon', ['xy'])),
    # 'MultiPolygon':       Spec('',  '',  '[1]',  '+',  C('+', 'polygon', ['xy'])),
    'Trajectory':         Spec('',  '',  '[1]',  '',   C('+', 'tuple', ['txyz', 'txy'])),
    # 'Section':            Spec('',  '',   '+',   '',   C('+', 'tuple', ['txy'])),
}

def get_random_domain():
    ''' Returns a random domain of a random domain type '''

    domain_type = random.choice(list(DOMAIN_TYPES.keys()))
    return get_random_domain_of_type(domain_type)


def get_random_domain_of_type(domain_type):
    ''' Returns a random domain of the specified domain type '''

    time_values = ["2008-01-01T04:00:00Z",
                   "2008-01-01T05:00:00Z",
                   "2008-01-01T06:00:00Z"]
    numeric_values = [1, 2, 3]

    spec = DOMAIN_TYPES[domain_type]._asdict()
    axes = {}
    for name, info in spec.items():
        if info == '':
            continue
        if name in ['x', 'y', 'z', 't']:
            cardinality = info
            if name == 't':
                values = time_values
            else:
                values = numeric_values
            single = { 'values': [values[0]] }
            multi = { 'values': values[:random.randint(1, len(values))] }

            if cardinality == '1':
                axes[name] = single
            elif cardinality == '+':
                axes[name] = multi
            elif cardinality == '[1]':
                if random.random() < 0.5:
                    axes[name] = single
            elif cardinality == '[+]':
                if random.random() < 0.5:
                    axes[name] = multi
            else:
                assert False, "Invalid axis cardinality"
        elif name == 'composite':
            existing_axes = list(axes.keys())
            possible_coordinates = [
                c for c in info.coordinates
                if set(c) & set(existing_axes) == set()
            ]
            coordinates = list(random.choice(possible_coordinates))
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
                values = values[:random.randint(1, len(values))]
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
    
    return domain
