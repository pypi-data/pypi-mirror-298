import math
from collections import namedtuple

import pytest

from funk_py.modularity.basic_structures import ObjAttributeError, Obj


NEWLINE = '\n'


def set_attr(obj, key, value): obj.__setattr__(key, value)


def set_item(obj, key, value): obj[key] = value


def direct_set_item(obj, key, value): obj.__setitem__(key, value)


BASIC_ADD_LAMBDAS = (set_item, set_attr, direct_set_item)
BASIC_ADD_LAMBDA_NAMES = ('setting an item', 'setting an attribute',
                          'setting an item by directly calling __setitem__')


@pytest.fixture(params=BASIC_ADD_LAMBDAS, ids=BASIC_ADD_LAMBDA_NAMES)
def add_methods(request): return request.param


def del_attr(obj, key): obj.__delattr__(key)


def del_item(obj, key): obj.__delitem__(key)


BASIC_DEL_LAMBDAS = (del_item, del_attr)
BASIC_DEL_LAMBDA_NAMES = ('deleting an item', 'deleting an attribute')


@pytest.fixture(params=BASIC_DEL_LAMBDAS, ids=BASIC_DEL_LAMBDA_NAMES)
def del_methods(request): return request.param


def get_attr(obj, key): return obj.__getattr__(key)


def get_item(obj, key): return obj.__getitem__(key)


BASIC_GET_LAMBDAS = (get_item, get_attr)
BASIC_GET_LAMBDA_NAMES = ('getting an item', 'getting an attribute')


@pytest.fixture(params=BASIC_GET_LAMBDAS, ids=BASIC_GET_LAMBDA_NAMES)
def get_methods(request): return request.param


SIMPLE_VALS1 = (1, 'lorem', math.pi)
SIMPLE_VALS2 = (2, 'ipsum', math.inf)
SIMPLE_VAL_NAMES = ('int', 'str', 'flt')
SIMPLE_KEYS = tuple(c for c in 'abcdefghijklmnopqrstuvwxyz')
ODD_VAL_OUT = 17.77777


EXTRA_VALUE_SET = (3, 'dolor', -0)
SIMPLE_KEYS1 = SIMPLE_KEYS[:len(SIMPLE_VALS1)]
SIMPLE_KEYS2 = SIMPLE_KEYS[len(SIMPLE_VALS1): len(SIMPLE_VALS1) + len(SIMPLE_VALS2)]
EXTRA_KEYS = SIMPLE_KEYS[len(SIMPLE_VALS1) + len(SIMPLE_VALS2):
                         len(SIMPLE_VALS1) + len(SIMPLE_VALS2) + len(EXTRA_VALUE_SET)]


@pytest.fixture
def odd_key_out(): return SIMPLE_KEYS[-1]


@pytest.fixture
def odd_val_out(): return ODD_VAL_OUT


@pytest.fixture
def regular_dict(): return dict(zip(EXTRA_KEYS, EXTRA_VALUE_SET))


@pytest.fixture
def regular_dict2(): return dict(zip(SIMPLE_KEYS2, SIMPLE_VALS1))


@pytest.fixture
def iterable_dict(): return tuple(zip(EXTRA_KEYS, EXTRA_VALUE_SET))


@pytest.fixture
def nested_dict(): return dict(zip((*SIMPLE_KEYS1, SIMPLE_KEYS[-1]), (*SIMPLE_VALS1, {})))


BAD_ATTR_MSG = ('The correct value was retrieved by index, but the same value was not retrieved '
                ' via attribute. There may be a problem with __getattr__.')
BAD_ITEM_MSG = ('Getting the stored value via attribute succeeded, but the same value was not '
                ' retrieved by index. There may be a problem with __getitem__.')
BAD_ATTR_ITEM_MSG = ('A match was retrieved by neither attribute nor index; however, the correct '
                     ' value was actually stored. Both__getitem__ and __getattr__ have a '
                     ' problem.')
WRONG_ITEM_STORED = ('The wrong value was stored. Normal access methods were bypassed to confirm '
                     ' this.')
WRONG_START = 'Test Invalid: expected Obj not generated!'


def confirm_expected_storage(testy, key, val, add_msg: str = ''):
    # Since we have two expected ways to get the value we stored out, we'll see if either of them
    # works. That way a false fail on this test due to a broken __getattr__ or __getitem__ can be
    # properly-diagnosed.
    ans1 = testy.__getattr__(key) == val
    if not ans1:
        ans2 = testy[key] == val
        if not ans2:
            assert dict.__getitem__(testy, key) == val, \
                add_msg + (NEWLINE if add_msg else '') + WRONG_ITEM_STORED
            assert False, add_msg + BAD_ATTR_ITEM_MSG

        assert False, add_msg + BAD_ATTR_MSG

    assert testy[key] == val, add_msg + BAD_ITEM_MSG


def safe_confirm_expected_storage(testy, key, val, add_msg: str = ''):
    assert dict.__getitem__(testy, key) == val, (
            add_msg + (NEWLINE if add_msg else '') + WRONG_ITEM_STORED)


def multi_confirm_expected_storage(testy, source, add_msg: str = ''):
    for key, val in source:
        if isinstance(val, dict):
            o_val = dict.__getitem__(testy, key)
            if not isinstance(o_val, Obj):
                assert not isinstance(o_val, dict), (f'{add_msg}{NEWLINE if add_msg else ""}'
                                                     f'Expected: {repr(val)}\n'
                                                     f'Actual: {repr(o_val)}')
                assert False, (f'{add_msg}{NEWLINE if add_msg else ""}'
                               f'Expected: {repr(val)}\n'
                               f'Actual: {repr(o_val)}')

            multi_confirm_expected_storage(o_val, val.items(), add_msg)

        else:
            confirm_expected_storage(testy, key, val, add_msg)


def safe_multi_confirm_expected_storage(testy, source, add_msg: str = ''):
    for key, val in source:
        if isinstance(val, dict):
            o_val = dict.__getitem__(testy, key)
            if not isinstance(o_val, Obj):
                assert not isinstance(o_val, dict), (f'{add_msg}{NEWLINE if add_msg else ""}'
                                                     f'Expected: {repr(val)}\n'
                                                     f'Actual: {repr(o_val)}')
                assert False, (f'{add_msg}{NEWLINE if add_msg else ""}'
                               f'Expected: {repr(val)}\n'
                               f'Actual: {repr(o_val)}')

            safe_multi_confirm_expected_storage(o_val, val.items(), add_msg)

        else:
            safe_confirm_expected_storage(testy, key, val, add_msg)


def confirm_expected_storage_size(testy, expected_len):
    # This test is written to test both the dict.__len__ and Obj.__len__, which should be one and
    # the same. ORDER OF LINES SHOULD BE MAINTAINED.

    # Gather this data to present a clear image of the situation after an assertion. Do this before
    # everything to get a (hopefully) pristine image of the Obj.
    inner_data0 = dict(dict.items(testy))

    # We get dict.__len__ first, to minimize chance of mutation from a mistake in an overridden
    # __len__ method should someone determine it is justified. If a change is made that
    # intentionally makes Obj.__len__ reflect a different length from dict.__len__ this may be
    # removed. Keep in mind all error messages should be adjusted appropriately in this case.
    dict_len = dict.__len__(testy)
    # Obj.__len__ is then used to verify that it performs correctly. It will be compared to
    # dict.__len__ to make sure that it is working as normal dict.__len__ would.
    obj_len = len(testy)

    # Gather this data to present a clear image of the situation after an assertion. Do this after
    # the first __len__ check.
    inner_data1 = dict(dict.items(testy))

    # We get dict.__len__ after Obj.__len__ has been called in order to check for potential
    # unintended mutation caused by calling Obj.__len__. This is because the class messes with
    # attributes, which can cause unintentional side effects when done wrong.
    dict_after_len = dict.__len__(testy)
    # We get Obj.__len__ last to ensure no unexpected nonsense is occurring under the hood. It will
    # again be compared to dict.__len__ thusly allowing almost complete certainty of correct
    # behavior.
    obj_after_len = len(testy)

    # It's unlikely that this will ever be needed, but just in case of unexpected strange behavior,
    # it shall be collected. Don't use copy. I honestly forget why, but just don't.
    inner_data2 = dict(dict.items(testy))

    def err_msg(msg, d_len, o_len, state, prev_state):
        # It may be beneficial to add all len measurements, but data is limited as much as is
        # reasonable
        return msg + (f'\nLength according to dict.__len__: {d_len}\n'
                      f'Length according to Obj.__len__: {o_len}\n'
                      f'Expected length: {expected_len}\n'
                      f'Data in dict before measurement: {prev_state}\n'
                      f'Data in dict after measurement: {state}')

    if dict_len != obj_len:
        if dict_len == expected_len:
            assert False, err_msg('Obj.__len__ returned the length despite dict.__len__ '
                                  ' retrieving the right value. This method should generally not '
                                  ' be overridden since it is safer to let the regular __len__ '
                                  ' method of dict handle it for us.',
                                  dict_len, obj_len, inner_data1, inner_data0)

        elif obj_len != expected_len:
            assert False, err_msg('Obj.__len__ returned the expected length,but does not reflect'
                                  ' the actual data stored in the instance.',
                                  dict_len, obj_len, inner_data1, inner_data0)

        else:
            assert False, err_msg('Obj.__len__ and dict.__len__ both returned unexpected lengths '
                                  ' that did not match. Most likely, something is wrong:\n'
                                  '1: With initialization of the class or with methods that were '
                                  ' tested during this run.\n'
                                  '2: With the Obj.__len__ method. This method should generally not'
                                  ' be overridden since it is safer to let the regular __len__'
                                  ' method of dict handle it for us.',
                                  dict_len, obj_len, inner_data1, inner_data0)

    elif obj_len != expected_len:
        assert False, err_msg('Both Obj.__len__ and dict.__len__ returned the wrong length. Most '
                              ' likely, something is wrong with initialization of the class or '
                              ' with methods that were tested during this run.',
                              dict_len, obj_len, inner_data1, inner_data0)

    elif dict_after_len != obj_after_len:
        if dict_after_len == expected_len:
            assert False, err_msg('Obj.__len__ returned the correct length the first time, but '
                                  ' failed to return the correct value the second time. '
                                  ' dict.__len__ somehow got the expected value, though,which '
                                  ' leads me to the conclusion that,unless you intended to do '
                                  ' this, you are a wizard. Good for you...',
                                  dict_after_len, obj_after_len, inner_data2, inner_data1)

        elif obj_after_len != expected_len:
            assert False, err_msg('Obj.__len__ and dict.__len__ both returned the expected length '
                                  ' the first time, but both failed to do so the second time... '
                                  ' as well as disagreeing with each other. This leads me to the '
                                  ' conclusion that, unless you intended to do this, you are a arch'
                                  ' mage. Good for you...',
                                  dict_after_len, obj_after_len, inner_data2, inner_data1)

        else:
            assert False, err_msg('Obj.__len__ returned the expected length both the first time '
                                  ' and the second time, but does not reflect the actual data '
                                  ' stored in the instance the second time. You will need to '
                                  ' analyze the code in the class to determine what is causing '
                                  ' this.',
                                  dict_after_len, obj_after_len, inner_data2, inner_data1)

    elif obj_after_len != expected_len:
        assert False, err_msg('__len__ generated a key when it shouldn\'t have. This likely means '
                              ' that __len__ may need to be added to _HIDE_THESE. It is also '
                              ' advisable to check if the same issue is occurring with other'
                              ' methods, since it means that python has begun working differently'
                              ' from how it previously worked. There is a chance that the __len__'
                              ' method was deleted from the class.',
                              dict_after_len, obj_after_len, inner_data2, inner_data1)


class TestCreation:
    def test_can_be_created_empty(self):
        testy = Obj()
        confirm_expected_storage_size(testy, 0)

    def test_can_be_created_with_regular_dict(self, regular_dict):
        testy = Obj(regular_dict)
        # Do a read of the values in the Obj to verify the expected Obj was created.
        confirm_expected_storage_size(testy, len(regular_dict))
        multi_confirm_expected_storage(testy, regular_dict.items())

    def test_can_be_created_with_iterable(self, iterable_dict):
        testy = Obj(iterable_dict)
        # Do a read of the values in the Obj to verify the expected Obj was created.
        confirm_expected_storage_size(testy, len(iterable_dict))
        multi_confirm_expected_storage(testy, iterable_dict)

    def test_can_be_created_with_kwargs(self, regular_dict):
        testy = Obj(**regular_dict)
        # Do a read of the values in the Obj to verify the expected Obj was created.
        confirm_expected_storage_size(testy, len(regular_dict))
        multi_confirm_expected_storage(testy, regular_dict.items())

    def test_can_be_created_with_regular_dict_and_kwargs(self, regular_dict,
                                                         regular_dict2):
        testy = Obj(regular_dict, **regular_dict2)
        # Do a read of the values in the Obj to verify the expected Obj was created.
        confirm_expected_storage_size(testy, len(regular_dict) + len(regular_dict2))
        multi_confirm_expected_storage(testy, regular_dict.items())
        multi_confirm_expected_storage(testy, regular_dict2.items())

    def test_can_be_created_with_iterable_and_kwargs(self, iterable_dict,
                                                     regular_dict2):
        testy = Obj(iterable_dict, **regular_dict2)
        # Do a read of the values in the Obj to verify the expected Obj was created.
        confirm_expected_storage_size(testy,
                                      len(iterable_dict) + len(regular_dict2))
        multi_confirm_expected_storage(testy, iterable_dict)
        multi_confirm_expected_storage(testy, regular_dict2.items())

    def test_can_be_created_with_nested(self, nested_dict):
        testy = Obj(nested_dict)
        # Do a read of the values in the Obj to verify the expected Obj was created.
        confirm_expected_storage_size(testy, len(nested_dict))
        multi_confirm_expected_storage(testy, nested_dict.items())


@pytest.fixture(params=SIMPLE_VALS1,
                ids=tuple('value=' + v for v in SIMPLE_VAL_NAMES))
def simple_values(request): return request.param


@pytest.fixture(params=SIMPLE_VALS2,
                ids=tuple('key=' + v for v in SIMPLE_VAL_NAMES))
def weird_keys(request): return request.param


@pytest.fixture(params=SIMPLE_KEYS[:len(SIMPLE_VALS1)])
def simple_keys(request): return request.param


OverlapDef = namedtuple('OverlapDef', {'base', 'added', 'unhardened', 'hardened'})


SIMPLE_DICT_DEF = (SIMPLE_KEYS1, SIMPLE_VALS1)
SIMPLE_NESTED_DICT_DEF = (SIMPLE_KEYS1, (*SIMPLE_VALS1[:2], (SIMPLE_KEYS2, SIMPLE_VALS2)))


@pytest.fixture
def overlap_base_dict():
    return dict(zip(*SIMPLE_DICT_DEF))


@pytest.fixture(params=SIMPLE_KEYS1,
                ids=tuple(f'key={i + 1}' for i in range(len(SIMPLE_KEYS1))))
def overlap_keys(request):
    return request.param


@pytest.fixture(params=SIMPLE_VALS2,
                ids=tuple('value=' + v for v in SIMPLE_VAL_NAMES))
def overlap_vals(request):
    return request.param


def buildy_buildy_dict(iterable):
    builder = {}
    for k, v in zip(*iterable):
        if isinstance(v, tuple):
            builder[k] = buildy_buildy_dict(v)

        else:
            builder[k] = v

    return builder


# Regarding the following definitions, hardened only has to convey whether an
# error should be raised. When an error should not be raised, hardened Objs
# should get the same results as unhardened objects.
@pytest.fixture(params=(
    OverlapDef(base=SIMPLE_DICT_DEF,
               added=(SIMPLE_KEYS1,
                      SIMPLE_VALS2),
               unhardened=(SIMPLE_KEYS1,
                           SIMPLE_VALS2),
               hardened=...),
    OverlapDef(base=SIMPLE_DICT_DEF,
               added=(SIMPLE_KEYS1[:2],
                      SIMPLE_VALS2[:2]),
               unhardened=(SIMPLE_KEYS1,
                           (*SIMPLE_VALS2[:2],
                            SIMPLE_VALS1[2])),
               hardened=...),
    OverlapDef(base=SIMPLE_DICT_DEF,
               added=((*SIMPLE_KEYS1[1:],
                       SIMPLE_KEYS2[0]),
                      SIMPLE_VALS2),
               unhardened=((*SIMPLE_KEYS1,
                            SIMPLE_KEYS2[0]),
                           (SIMPLE_VALS1[0],
                            *SIMPLE_VALS2)),
               hardened=ObjAttributeError),
    OverlapDef(base=SIMPLE_DICT_DEF,
               added=(EXTRA_KEYS,
                      EXTRA_VALUE_SET),
               unhardened=((*SIMPLE_KEYS1,
                            *EXTRA_KEYS),
                           (*SIMPLE_VALS1,
                            *EXTRA_VALUE_SET)),
               hardened=ObjAttributeError),

    OverlapDef(base=SIMPLE_NESTED_DICT_DEF,
               added=(SIMPLE_KEYS1,
                      (*EXTRA_VALUE_SET[:2],
                       (SIMPLE_KEYS2,
                        SIMPLE_VALS1))),
               unhardened=(SIMPLE_KEYS1,
                           (*EXTRA_VALUE_SET[:2],
                            (SIMPLE_KEYS2,
                             SIMPLE_VALS1))),
               hardened=...),
    OverlapDef(base=SIMPLE_NESTED_DICT_DEF,
               added=(SIMPLE_KEYS1,
                      (*EXTRA_VALUE_SET[:2],
                       ((SIMPLE_KEYS2[0],),
                        (SIMPLE_VALS1[0],)))),
               unhardened=(SIMPLE_KEYS1,
                           (*EXTRA_VALUE_SET[:2],
                            (SIMPLE_KEYS2,
                             (SIMPLE_VALS1[0],
                              *SIMPLE_VALS2[1:])))),
               hardened=...),
    OverlapDef(base=SIMPLE_NESTED_DICT_DEF,
               added=(SIMPLE_KEYS1,
                      EXTRA_VALUE_SET),
               unhardened=(SIMPLE_KEYS1,
                           EXTRA_VALUE_SET),
               hardened=ObjAttributeError),

    OverlapDef(base=SIMPLE_NESTED_DICT_DEF,
               added=(SIMPLE_KEYS1[1:],
                      (EXTRA_VALUE_SET[1],
                       (SIMPLE_KEYS2,
                        SIMPLE_VALS1))),
               unhardened=(SIMPLE_KEYS1,
                           (SIMPLE_VALS1[0],
                            EXTRA_VALUE_SET[1],
                            (SIMPLE_KEYS2,
                             SIMPLE_VALS1))),
               hardened=...),
    OverlapDef(base=SIMPLE_NESTED_DICT_DEF,
               added=(SIMPLE_KEYS1[1:],
                      (EXTRA_VALUE_SET[0],
                       ((SIMPLE_KEYS2[0],),
                        (SIMPLE_VALS1[0],)))),
               unhardened=(SIMPLE_KEYS1,
                           (SIMPLE_VALS1[0],
                            EXTRA_VALUE_SET[0],
                            (SIMPLE_KEYS2,
                             (SIMPLE_VALS1[0],
                              *SIMPLE_VALS2[1:])))),
               hardened=...),
    OverlapDef(base=SIMPLE_NESTED_DICT_DEF,
               added=(SIMPLE_KEYS1[1:],
                      EXTRA_VALUE_SET[1:]),
               unhardened=(SIMPLE_KEYS1,
                           (SIMPLE_VALS1[0], *EXTRA_VALUE_SET[1:])),
               hardened=ObjAttributeError),
), ids=(
        'Full Overlap',
        'Smaller Overlap',
        'Partial Overlap (Both Sides Have Some Shared, but not All)',
        'Zero Overlap',
        'Full Overlap, Nested Full Overlap',
        'Full Overlap, Nested Smaller Overlap',
        'Full Overlap, Nested Replaced',
        'Smaller Overlap, Nested Full Overlap',
        'Smaller Overlap, Nested Smaller Overlap',
        'Smaller Overlap, Nested Replaced'
))
def update_overlap_dicts(request):
    def_ = request.param
    return OverlapDef(base=buildy_buildy_dict(def_.base),
                      added=buildy_buildy_dict(def_.added),
                      unhardened=buildy_buildy_dict(def_.unhardened),
                      hardened=def_.hardened)


class TestUnhardened:
    def test_adding_simple_values(self, simple_values, weird_keys, add_methods, regular_dict,
                                  regular_dict2, iterable_dict):
        def base_str(fill):
            return '<For an Obj created with ' + fill + '>'

        testy = Obj()
        add_methods(testy, weird_keys, simple_values)
        confirm_expected_storage(testy, weird_keys, simple_values, base_str('no args'))

        # created with regular dict
        testy = Obj(regular_dict)
        add_methods(testy, weird_keys, simple_values)
        confirm_expected_storage(testy, weird_keys, simple_values, base_str('regular dict'))
        multi_confirm_expected_storage(testy, regular_dict.items(), base_str('regular dict'))

        # created with kwargs
        testy = Obj(**regular_dict)
        add_methods(testy, weird_keys, simple_values)
        confirm_expected_storage(testy, weird_keys, simple_values, base_str('kwargs'))
        multi_confirm_expected_storage(testy, regular_dict.items(), base_str('kwargs'))

        # created with iterable
        testy = Obj(iterable_dict)
        add_methods(testy, weird_keys, simple_values)
        confirm_expected_storage(testy, weird_keys, simple_values, base_str('an iterable'))
        multi_confirm_expected_storage(testy, iterable_dict, base_str('an iterable'))

        # created with regular dict and kwargs
        testy = Obj(regular_dict, **regular_dict2)
        add_methods(testy, weird_keys, simple_values)
        confirm_expected_storage(testy, weird_keys, simple_values, base_str('a dict and kwargs'))
        multi_confirm_expected_storage(testy, regular_dict.items(), base_str('a dict and kwargs'))
        multi_confirm_expected_storage(testy, regular_dict2.items(), base_str('a dict and kwargs'))

        # created with iterable and kwargs
        testy = Obj(iterable_dict, **regular_dict2)
        add_methods(testy, weird_keys, simple_values)
        confirm_expected_storage(testy, weird_keys, simple_values,
                                 base_str('an iterable and kwargs'))
        multi_confirm_expected_storage(testy, iterable_dict, base_str('an iterable and kwargs'))
        multi_confirm_expected_storage(testy, regular_dict2.items(),
                                       base_str('an iterable and kwargs'))

    def test_changing_keys(self, overlap_base_dict, add_methods, overlap_keys, overlap_vals):
        testy = Obj(overlap_base_dict)
        add_methods(testy, overlap_keys, overlap_vals)
        confirm_expected_storage(testy, overlap_keys, overlap_vals)
        confirm_expected_storage_size(testy, len(overlap_base_dict))

    def test_update_works(self, update_overlap_dicts):
        # Verify it works without any prior reads.
        testy = Obj(update_overlap_dicts.base)
        testy.update(update_overlap_dicts.added)
        # Do a read of the values in the Obj to verify the expected Obj was created.
        multi_confirm_expected_storage(testy, update_overlap_dicts.unhardened.items())
        confirm_expected_storage_size(testy, len(update_overlap_dicts.unhardened))

    def test_del_works(self, overlap_base_dict, overlap_keys, del_methods):
        testy = Obj(overlap_base_dict)
        del_methods(testy, overlap_keys)
        # the dict.__getitem__ method is used here because we expect
        # Obj.__getitem__ and Obj.__getattr__ to mutate the Obj.
        assert dict.get(testy, overlap_keys, ...) is ..., \
            f'Deletion did not succeed for key {overlap_keys}.'

    def test_clear_works(self, regular_dict):
        testy = Obj(regular_dict)
        assert len(testy) == len(regular_dict), WRONG_START
        testy.clear()
        confirm_expected_storage_size(testy, 0)

    def test_missing_key_returns_new_obj(self, get_methods, odd_key_out):
        testy = Obj()
        assert dict.__len__(testy) == 0, \
            ('Initial Obj has elements when it should not. This indicates a failure in'
             ' instantiation.')
        ans1 = get_methods(testy, odd_key_out)
        assert isinstance(ans1, Obj), \
            ('The tested method did not result in a new instance of Obj being generated. Obj is'
             ' expected to generate a new object when it is not hardened and Obj.__getitem__ or'
             ' Obj.__getattr__ is called.')
        assert dict.__len__(ans1) == 0, \
            ('The tested method did generate a new instance of Obj. However, this instance was not'
             ' empty even though it should have been.')
        # Use dict.__getitem__ to ensure the item was actually added to testy.
        # Don't use a method of Obj to test this...
        assert isinstance(dict.__getitem__(testy, odd_key_out), Obj), \
            ('The tested method did generate a new instance of Obj. However, it was not actually'
             ' stored in the Obj.')

        # Get the item one more time to make sure it isn't automatically
        # overwritten for some reason.
        ans2 = get_methods(testy, odd_key_out)
        assert ans1 is ans2, \
            ('The tested method did generate a new instance of Obj. However, it was overwritten'
             ' when the mehtod was called again. There is a flaw in the logic that determines when'
             ' to generate a new Obj.')

    def test_pop_works(self, regular_dict):
        for key, val in regular_dict.items():
            copier = regular_dict.copy()
            testy = Obj(regular_dict)
            safe_multi_confirm_expected_storage(testy, copier.items(), WRONG_START)

            ans1 = testy.pop(key)
            ans2 = copier.pop(key)
            if ans1 != val:
                if ans1 == ans2:
                    assert False, (f'Somehow, the wrong value was popped, there may be an issue'
                                   f' with how the test is written.\n'
                                   f'Both Obj.pop({repr(key)}) and dict.pop({repr(key)}) returned'
                                   f' {repr(ans1)}.\n'
                                   f'Expected value was {repr(val)}.')

                elif ans2 != val:
                    assert False, (f'Somehow, a different value was popped from the source dict and'
                                   f' the Obj. There may be an issue with how the test is written.'
                                   f'\n'
                                   f'Obj.pop({repr(key)}) returned {repr(ans1)}.\n'
                                   f'dict.pop({repr(key)}) returned {repr(ans2)}.\n'
                                   f'Expected value was {repr(val)}.')

            safe_multi_confirm_expected_storage(testy, copier.items(),
                                                f'Objects didn\'t agree despite'
                                                f' Obj.pop({repr(key)}) returning the expected'
                                                f' value.')

    def test_popitem_works(self, regular_dict):
        # Technically, if this works, dict does maintain order.
        testy = Obj(regular_dict)
        copier = regular_dict.copy()
        safe_multi_confirm_expected_storage(testy, copier.items(), WRONG_START)
        for item in reversed(regular_dict.items()):
            ans1 = testy.popitem()
            ans2 = copier.popitem()
            if ans1 != item:
                if ans1 == ans2:
                    assert False, (f'Somehow, the wrong item was popped, there may be an issue'
                                   f' with how the test is written.\n'
                                   f'Both Obj.popitem() and dict.popitem() returned {repr(ans1)}.\n'
                                   f'Expected value was {repr(item)}.')

                elif ans2 != item:
                    assert False, (f'Somehow, a different item was popped from the source dict and'
                                   f' the Obj. There may be an issue with how the test is written.'
                                   f'\n'
                                   f'Obj.popitem() returned {repr(ans1)}.\n'
                                   f'dict.popitem() returned {repr(ans2)}.\n'
                                   f'Expected value was {repr(item)}.')

            safe_multi_confirm_expected_storage(testy, copier.items(),
                                                'Objects didn\'t agree despite Obj.popitem()'
                                                ' returning the expected value.')


class TestHardened:
    def test_adding_new_fails(self, add_methods, odd_key_out, odd_val_out):
        testy = Obj()
        testy.harden()
        with pytest.raises(ObjAttributeError) as e_info:
            add_methods(testy, odd_key_out, odd_val_out)

        # Make sure the object didn't get mutated during the bad set event.
        assert dict.__len__(testy) == 0, 'The Obj was mutated when the exception occurred!'

    def test_changing_keys(self, overlap_base_dict, add_methods, overlap_keys,
                           overlap_vals):
        testy = Obj(overlap_base_dict)
        testy.harden()
        add_methods(testy, overlap_keys, overlap_vals)
        confirm_expected_storage(testy, overlap_keys, overlap_vals)
        confirm_expected_storage_size(testy, len(overlap_base_dict))

    def test_update_works(self, update_overlap_dicts):
        # Verify it works without any prior reads.
        testy = Obj(update_overlap_dicts.base)
        testy.harden()
        if update_overlap_dicts.hardened is not ...:
            with pytest.raises(update_overlap_dicts.hardened):
                testy.update(update_overlap_dicts.added)

            # Make sure the object didn't get mutated during the bad update
            # event.
            assert dict.__len__(testy) == len(update_overlap_dicts.base), \
                'The Obj was mutated when the exception occurred!'

        else:
            testy.update(update_overlap_dicts.added)
            # Do a read of the values in the Obj to verify the expected Obj was
            # created.
            multi_confirm_expected_storage(testy, update_overlap_dicts.unhardened.items())
            confirm_expected_storage_size(testy, len(update_overlap_dicts.unhardened))

    def test_del_fails(self, overlap_base_dict, overlap_keys, del_methods):
        testy = Obj(overlap_base_dict)
        testy.harden()
        with pytest.raises(ObjAttributeError):
            del_methods(testy, overlap_keys)

        # the dict.__getitem__ method is used here because we expect
        # Obj.__getitem__ and Obj.__getattr__ to mutate the Obj.
        assert dict.get(testy, overlap_keys, ...) is not ..., \
            'Hardening did not prevent deletion, but did raise the expected exception.'

    def test_clear_fails(self, regular_dict):
        testy = Obj(regular_dict)
        testy.harden()
        assert dict.__len__(testy) == len(regular_dict), 'Test Invalid: expected Obj not generated!'
        with pytest.raises(ObjAttributeError):
            testy.clear()

        multi_confirm_expected_storage(testy, regular_dict.items(),
                                       'Hardening didn\'t prevent clearing completely, but did'
                                       ' raise the expected exception.')

    def test_missing_key_fails(self, get_methods):
        testy = Obj()
        testy.harden()
        assert dict.__len__(testy) == 0, \
            ('Initial Obj has elements when it should not. This indicates a failure in'
             ' instantiation.')
        with pytest.raises(ObjAttributeError):
            ans1 = get_methods(testy, SIMPLE_KEYS[-1])

        assert dict.__len__(testy) == 0, \
            ('Even though it did raise the expected exception, getting a value generated a new'
             ' key-val pair.')

    def test_pop_fails(self, regular_dict):
        testy = Obj(regular_dict)
        testy.harden()
        safe_multi_confirm_expected_storage(testy, regular_dict.items(), WRONG_START)

        for key, val in regular_dict.items():
            ans = ...
            with pytest.raises(ObjAttributeError):
                ans = testy.pop(key)

            assert ans is ..., (f'Obj.pop still returned something even though the Obj was '
                                f'hardened.\n'
                                f'Returned {repr(ans)}.')
            safe_multi_confirm_expected_storage(testy, regular_dict.items(),
                                                f'Obj.pop did not return anything, but still '
                                                f'deleted the key.\n'
                                                f'Deleted key {repr(key)}')

    def test_popitem_fails(self, regular_dict):
        testy = Obj(regular_dict)
        testy.harden()
        safe_multi_confirm_expected_storage(testy, regular_dict.items(), WRONG_START)
        ans = ...
        with pytest.raises(ObjAttributeError):
            ans = testy.popitem()

        assert ans is ..., (f'Obj.popitem still returned something even though the Obj was '
                            f'hardened.\n'
                            f'Returned {repr(ans)}.')
        safe_multi_confirm_expected_storage(testy, regular_dict.items(),
                                            f'Obj.pop did not return anything, but still deleted '
                                            f'an item.')
