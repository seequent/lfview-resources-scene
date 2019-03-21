import numpy as np
import properties
import pytest

from lfview.resources import scene


def test_light():
    light = scene.Light(
        direction='up',
        brightness=1.,
        enabled=True,
        uid='something',
    )
    assert light.validate()


def test_slice():
    slic = scene.Slice(
        normal='east',
        mode='section',
    )
    assert slic.validate()
    slic.position_b = properties.undefined
    with pytest.raises(properties.ValidationError):
        slic.validate()
    slic.position_b = [0., 0, 0]
    slic.color_b = properties.undefined
    with pytest.raises(properties.ValidationError):
        slic.validate()
    slic.mode = 'normal'
    assert slic.validate()


def test_slicegroup():
    group = scene.SliceGroup(
        slices=[{
            'normal': 'east',
            'mode': 'normal',
        }],
        uid='group',
    )
    assert group.validate()


def test_ruler():
    ruler = scene.Ruler(
        positions=[[0., 0., 0.], [1., 1., 1.]],
        objects=[
            'https://example.com/api/elements/pointset/abc123',
            'https://example.com/api/elements/surface/def456',
        ]
    )
    assert ruler.validate()


def test_camerastandard():
    camera = scene.CameraStandard(
        mode='perspective',
        target='zero',
        radius=1.,
        zoom=1.,
        rotation=[0., 0., 0., 0.],
    )
    assert camera.validate()


def test_base_element_view():
    view = scene.scene._BaseElementView(
        element='https://example.com/api/elements/pointset/abc123',
        slice_group='group',
    )
    assert view.validate()


def test_plot():
    plot = scene.Plot(views=[])
    assert plot.validate()


def test_scene():
    my_scene = random_scene()
    assert my_scene.validate()


def random_float_generator():
    while True:
        yield np.random.random()


def random_scene():
    r = random_float_generator()
    my_scene = scene.Scene(
        lights=[
            scene.Light(
                brightness=next(r),
                direction=[next(r), next(r), next(r)],
                enabled=True,
            ) for i in range(4)
        ],
        camera=scene.CameraStandard(
            mode='orthographic',
            radius=next(r),
            rotation=[next(r), next(r), next(r),
                      next(r)],
            target=[next(r), next(r), next(r)],
            up_direction=[next(r), next(r), next(r)],
            zoom=next(r),
        ),
        plots=[
            scene.Plot(
                position=[next(r), next(r), next(r)],
                scale=[next(r), next(r), next(r)],
                rotation=[next(r), next(r), next(r),
                          next(r)],
                lims=[
                    [next(r), next(r)],
                    [next(r), next(r)],
                    [next(r), next(r)],
                ],
                exaggeration=[
                    int(val * 10 + 1)
                    for val in [next(r), next(r), next(r)]
                ],
                slice_groups=[
                    scene.SliceGroup(
                        slices=[
                            scene.Slice(
                                position_a=[next(r), next(r),
                                            next(r)],
                                position_b=[next(r), next(r),
                                            next(r)],
                                normal=[next(r), next(r),
                                        next(r)],
                                mode='reversed',
                                color_a='red',
                                color_b='red',
                            ),
                        ],
                        style='intersection',
                    )
                ],
                measurements=[
                    scene.Ruler(
                        positions=[
                            [next(r), next(r), next(r)],
                            [next(r), next(r), next(r)],
                        ],
                        objects=[
                            'https://example.com/api/elements/pointset/abc123',
                            'https://example.com/api/elements/pointset/abc123',
                        ],
                    )
                ],
                views=[
                    scene.Surface(
                        visible=True,
                        opacity={
                            'value': 0.5,
                            'data': 'https://example.com/api/data/basic/abc123',
                            'mapping': 'https://example.com/api/mappings/continuous/abc123',
                        },
                        color={
                            'value': 'r',
                            'back': 'r',
                            'data': 'https://example.com/api/data/basic/abc123',
                            'mapping': 'https://example.com/api/mappings/continuous/abc123',
                        },
                        wireframe={
                            'active': True,
                        },
                        textures=[
                            {
                                'data': 'https://example.com/api/textures/projection/abc123'
                            },
                        ],
                        element=
                        'https://example.com/api/elements/surface/abc123',
                    ) for i in range(5)
                ],
            )
        ]
    )
    return my_scene
