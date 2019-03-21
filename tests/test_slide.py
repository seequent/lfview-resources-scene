from random import randint

import properties
import pytest
from six import string_types

from lfview.resources import scene

from .test_scene import random_scene, random_float_generator


def test_base_types():
    assert scene.Slide.BASE_TYPE == 'slides'
    assert scene.Feedback.BASE_TYPE == 'feedback'


def test_scene_registry():
    assert scene.SCENE_REGISTRY['Slide'] is scene.Slide
    assert scene.SCENE_REGISTRY['Feedback'] is scene.Feedback


@pytest.mark.parametrize('test_uid', ['{base}/az78fet7vfr8v'])
@pytest.mark.parametrize('test_class', [scene.Feedback, scene.Slide])
def test_validates_correct_uids(test_class, test_uid):
    assert test_class.validate_uid(test_uid.format(base=test_class.BASE_TYPE))


@pytest.mark.parametrize(
    'test_uid', [
        '{base}/az02AZ',
        'az78fet7vfr8v/az78fet7vfr8v',
        '{base}/az78fet7vfr8v/az78fet7vfr8v',
    ]
)
@pytest.mark.parametrize('test_class', [scene.Feedback, scene.Slide])
def test_does_not_validate_incorrect_uids(test_class, test_uid):
    with pytest.raises(properties.ValidationError):
        test_class.validate_uid(test_uid.format(base=test_class.BASE_TYPE))


def test_feedback():
    instance = scene.Feedback()
    with pytest.raises(properties.ValidationError):
        instance.comment = 'a' * 5001
        instance.validate()
    instance.comment = 'a' * 5000
    assert instance.validate()


def test_annotationtext():
    instance = scene.AnnotationText(position=[0., 0.], color='b')
    with pytest.raises(properties.ValidationError):
        instance.comment = 'a' * 5001
        instance.validate()
    instance.comment = 'a' * 5000
    assert instance.validate()


def test_annotationink():
    anno = scene.AnnotationInk(
        position=[0., 0],
        color='g',
        path=[],
    )
    assert anno.validate()
    anno.path = [[0., 0.]] * 2001
    with pytest.raises(properties.ValidationError):
        anno.validate()


def test_slide():
    r = random_float_generator()
    slide = scene.Slide(
        scene=random_scene(),
        name='a' * 200,
        description='a' * 2000,
        annotation_plane={
            'origin': [next(r), next(r), next(r)],
            'axis_u': [next(r), next(r), next(r)],
            'axis_v': [next(r), next(r), next(r)],
        },
        annotations=[
            scene.AnnotationInk(
                uid=str(next(r)),
                position=[next(r), next(r)],
                color='r',
                path=[[next(r), next(r)] for i in range(500)],
            ) for i in range(10)
        ] + [
            scene.AnnotationText(
                uid=str(next(r)),
                position=[next(r), next(r)],
                color='r',
                comment=str(next(r)),
            ) for i in range(10)
        ],
    )
    assert slide.validate()
    s = slide.serialize()
    assert [isinstance(s[key], string_types) for key in s]
