"""Techniques module tests."""

import unittest

from namebot import techniques


class SliceEndsTestCase(unittest.TestCase):

    def test_oneletter(self):
        res = techniques.slice_ends('flabbergasted', count=1)
        self.assertEqual(res, 'labbergaste')

    def test_twoletter(self):
        res = techniques.slice_ends('flabbergasted', count=2)
        self.assertEqual(res, 'abbergast')

    def test_threeletter(self):
        res = techniques.slice_ends('flabbergasted', count=3)
        self.assertEqual(res, 'bbergas')

    def test_fourletter(self):
        res = techniques.slice_ends('flabbergasted', count=4)
        self.assertEqual(res, 'berga')

    def test_empty(self):
        res = techniques.slice_ends('flabbergasted', count=0)
        self.assertEqual(res, 'flabbergasted')

    def test_none(self):
        res = techniques.slice_ends('flabbergasted', count=None)
        self.assertEqual(res, 'flabbergasted')


class DomainifyTestCase(unittest.TestCase):

    def test_threeletter(self):
        self.assertEqual(techniques.domainify(['intercom']), ['inter.com'])

    def test_twoletter(self):
        self.assertEqual(
            techniques.domainify(['actively'], tld='.ly'), ['active.ly'])

    def test_fourletter(self):
        self.assertEqual(
            techniques.domainify(['scamp'], tld='.camp'), ['s.camp'])

    def test_empty(self):
        self.assertEqual(
            techniques.domainify(['intercom'], tld=''), ['intercom'])


class PalindromeTestCase(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(techniques.palindrome('Fool'), 'FoollooF')

    def test_complicated(self):
        self.assertEqual(techniques.palindrome(
            'Aardvarks'), 'AardvarksskravdraA')

    def test_spaced(self):
        self.assertEqual(techniques.palindrome(
            'Red Dragon'), 'Red DragonnogarD deR')

    def test_simple_array(self):
        self.assertEqual(techniques.palindromes(
            ['wtf', 'omg']), ['wtfftw', 'omggmo'])

    def test_simple_array_spaced(self):
        self.assertEqual(techniques.palindromes(
            ['wtf omg', 'omg wtf']), ['wtf omggmo ftw', 'omg wtfftw gmo'])

    def test_single_letter(self):
        self.assertEqual(techniques.palindrome('f'), 'ff')


class SpoonerismTestCase(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(
            techniques.spoonerism(['flim', 'boom', 'dang', 'dune']),
            ['blim foom', 'doom bang', 'dang dune'])

    def test_single_word(self):
        with self.assertRaises(ValueError):
            self.assertEqual(techniques.spoonerism(['foo']))


class KniferismTestCase(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(
            techniques.kniferism(['flim', 'boom', 'dang', 'dune']),
            ['flom boim', 'bonm daog', 'dang dune'])

    def test_single_word(self):
        with self.assertRaises(ValueError):
            self.assertEqual(techniques.kniferism(['foo']))


class ForkerismTestCase(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(
            techniques.forkerism(['flim', 'boom', 'dang', 'dune']),
            ['flim boom', 'boog danm', 'dane dung'])

    def test_single_word(self):
        with self.assertRaises(ValueError):
            self.assertEqual(techniques.forkerism(['foo']))


class ReduplicationAblautTestCase(unittest.TestCase):

    def test_vowel_a(self):
        self.assertEqual(techniques.reduplication_ablaut(
            ['cat', 'dog'], random=False, vowel='a'), ['dog dag'])

    def test_vowel_e(self):
        self.assertEqual(techniques.reduplication_ablaut(
            ['cat', 'dog'], random=False, vowel='e'),
            ['cat cet', 'dog deg'])

    def test_vowel_i(self):
        self.assertEqual(techniques.reduplication_ablaut(
            ['cat', 'dog'], random=False, vowel='i'),
            ['cat cit', 'dog dig'])

    def test_vowel_o(self):
        self.assertEqual(techniques.reduplication_ablaut(
            ['cat', 'dog'], random=False, vowel='o'), ['cat cot'])

    def test_vowel_u(self):
        self.assertEqual(techniques.reduplication_ablaut(
            ['cat', 'dog'], random=False, vowel='u'),
            ['cat cut', 'dog dug'])


class AffixWordsTestCase(unittest.TestCase):

    def setUp(self):
        self.words = ['shop']

    def test_prefix(self):
        res = techniques.prefixify(self.words)
        self.assertEqual(res[:3], ['ennishop', 'epishop', 'equishop'])

    def test_suffix(self):
        res = techniques.suffixify(self.words)
        self.assertEqual(res[:3], ['shopage', 'shopable', 'shopible'])

    def test_duplifix(self):
        res = techniques.duplifixify(self.words)
        self.assertEqual(res[:3], ['shop ahop', 'shop bhop', 'shop chop'])

    def test_duplifix_duplicates(self):
        res = techniques.duplifixify(self.words)
        self.assertTrue('shop shop' not in res)

    def test_disfix(self):
        words = ['propagating', 'gigantic']
        res = techniques.disfixify(words)
        self.assertEqual(res, ['pagating', 'antic'])

    def test_disfix_nosingle_pairs(self):
        words = ['shop', 'prop']
        res = techniques.disfixify(words)
        self.assertEqual(res, ['shop', 'prop'])

    def test_disfix_novowels(self):
        words = ['shp', 'prp']
        res = techniques.disfixify(words)
        self.assertEqual(res, words)

    def test_disfix_noconsonants(self):
        words = ['oooaeoa']
        res = techniques.disfixify(words)
        self.assertEqual(res, words)

    def test_infix(self):
        words = ['sophisticated']
        res = techniques.infixify(words)
        expected = ['sophistiqacated', 'sophistiqecated',
                    'sophistiqicated', 'sophistiqocated']
        self.assertEqual(res[0:4], expected)

    def test_infix_novowels(self):
        words = ['shp', 'prp']
        res = techniques.infixify(words)
        self.assertEqual(res, words)

    def test_infix_noconsonants(self):
        words = ['oooaeoa']
        res = techniques.infixify(words)
        self.assertEqual(res, words)

    def test_infix_nosingle_pairs(self):
        words = ['shop', 'prop']
        res = techniques.infixify(words)
        self.assertEqual(res, words)

    def test_simulfix(self):
        res = techniques.simulfixify(self.words)
        self.assertIsInstance(res, list)
        self.assertGreater(len(res), len(self.words))
        # Confirm that the pairs were added to each word
        for word in res:
            self.assertEqual(len(self.words[0]) + 2, len(word))

    def test_simulfix_custom_pairs(self):
        res = techniques.simulfixify(self.words, pairs=['ab', 'ec', 'oz'])
        self.assertEqual(res, ['shabop', 'shecop', 'shozop'])

    def test_simulfix_empty_strings(self):
        res = techniques.simulfixify(['', ''], pairs=['ab', 'ec'])
        self.assertEqual(res, ['ab', 'ec', 'ab', 'ec'])

    def test_simulfix_short_words(self):
        res = techniques.simulfixify(['f', 'b', 'a'], pairs=['ab', 'ec'])
        expected = ['abf', 'ecf', 'abb', 'ecb', 'aba', 'eca']
        self.assertEqual(res, expected)


class MakeFounderProductNameTestCase(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(
            techniques.make_founder_product_name(
                'Foo', 'Bar', 'Goods'), 'F & B Goods')

    def test_simple_lowercase(self):
        self.assertNotEqual(
            techniques.make_founder_product_name(
                'Foo', 'Bar', 'Goods'), 'foo bar & co goods')


class MakeNameAlliterationTestCase(unittest.TestCase):

    def test_simple(self):
        original = ['jamba', 'juice', 'dancing', 'tornado',
                    'disco', 'wicked', 'tomato']
        updated = ['dancing disco', 'disco dancing', 'jamba juice',
                   'juice jamba', 'tomato tornado', 'tornado tomato']
        self.assertEqual(
            techniques.make_name_alliteration(original), updated)

    def test_divider(self):
        original = ['content', 'applesauce', 'candor', 'character']
        updated = ['candor & character', 'candor & content',
                   'character & candor', 'character & content',
                   'content & candor', 'content & character']
        self.assertEqual(
            techniques.make_name_alliteration(
                original, divider=' & '), updated)


class MakeNameAbbreviationTestCase(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(
            techniques.make_name_abbreviation(
                ['Badische', 'Anilin', 'Soda', 'Fabrik']), 'BASF')


class MakeVowelTestCase(unittest.TestCase):

    def test_a(self):
        self.assertEqual(techniques.make_vowel(
            ['brad', 'angelina'], r'a{1}', 'a'), ['brangelina'])

    def test_e(self):
        self.assertEqual(techniques.make_vowel(
            ['street', 'credence'], r'e{1}', 'e'), ['stredence'])

    def test_i(self):
        self.assertEqual(techniques.make_vowel(
            ['stripe', 'wild'], r'i{1}', 'i'), ['strild'])

    def test_o(self):
        self.assertEqual(techniques.make_vowel(
            ['strode', 'pork'], r'o{1}', 'o'), ['strork'])

    def test_u(self):
        self.assertEqual(techniques.make_vowel(
            ['true', 'crude'], r'u{1}', 'u'), ['trude'])

    def test_no_substring(self):
        """Check for values that aren't found in the regex list."""
        self.assertEqual(techniques.make_vowel(
            ['matching', 'not'], r'a{1}', 'a'), [])


class MakePortmanteauDefaultVowelTestCase(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(
            techniques.make_portmanteau_default_vowel(
                ['sweet', 'potato', 'nifty', 'gadget', 'widgets']),
            ['potadget', 'gadgeet', 'widgeet'])


class MakemakePortmanteauSplitTestCase(unittest.TestCase):

    def test_2words(self):
        self.assertEqual(
            techniques.make_portmanteau_split(['dad', 'cool']),
            ['dadool', 'dadool', 'datool', 'dasool', 'dazool',
             'daxool', 'cocad', 'coad', 'colad', 'cotad',
             'cosad', 'cozad', 'coxad'])

    def test_results_count(self):
        self.assertEqual(
            len(techniques.make_portmanteau_split(
                ['dad', 'neat', 'cool'])), 40)
        self.assertEqual(
            len(techniques.make_portmanteau_split(
                ['dad', 'neat', 'cool', 'nifty'])), 58)
        self.assertEqual(
            len(techniques.make_portmanteau_split(
                ['dad', 'neat', 'cool', 'nifty', 'super', 'duper'])), 166)


class MakePunctuatorTestCase(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(
            techniques.make_punctuator(['delicious'], 'i'),
            ['deli-ci-ous', 'deli.ci.ous'])


class MakeVowelifyTestCase(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(
            techniques.make_vowelify(
                ['nautical', 'monster']), ['nautica', 'monste'])


class MakemisspellingTestCase(unittest.TestCase):

    def setUp(self):
        self.words = ['effects', 'phonics', 'glee', 'cron', 'chrono']
        self.expected = ['phonix', 'ephphects', 'gly', 'crawn', 'krono']

    def test_simple(self):
        res = techniques.make_misspelling(self.words)
        for word in self.expected:
            assert word in res


class PigLatinTestCase(unittest.TestCase):

    def test_simple(self):
        """Basic test."""
        self.assertEqual(
            techniques.pig_latinize(['rad']), ['adray'])

    def test_custom_postfix_value(self):
        """Basic test."""
        self.assertEqual(
            techniques.pig_latinize(['rad'], postfix='ey'), ['adrey'])

    def test_bad_postfix_value(self):
        """Basic test."""
        with self.assertRaises(TypeError):
            techniques.pig_latinize(['rad'], postfix=1223)


class AcronymLastnameTestCase(unittest.TestCase):

    def test_simple(self):
        desc = 'Amazingly cool product'
        self.assertEqual(
            'ACP McDonald', techniques.acronym_lastname(desc, 'McDonald'))

    def test_simple_nostopwords(self):
        desc = 'A cool product'
        self.assertEqual(
            'CP McDonald', techniques.acronym_lastname(desc, 'McDonald'))


class GetDescriptorsTestCase(unittest.TestCase):

    def test_complex(self):
        self.assertEqual(techniques.get_descriptors(
            ['Jumping', 'Fly', 'Monkey', 'Dog', 'Action']),
            {'VBG': ['Jumping'],
             'NNP': ['Fly', 'Monkey', 'Dog', 'Action']})


class MakeDescriptorsTestCase(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(techniques.make_descriptors(
            {'VBG': ['Jumping'], 'RB': ['Fly'],
             'NNP': ['Monkey', 'Dog', 'Action']}),
            ['Monkey Fly', 'Fly Monkey', 'Action Fly', 'Dog Fly',
             'Fly Dog', 'Fly Action'])


class AllPrefixesToFirstVowelTestCase(unittest.TestCase):

    def test_simple(self):
        word = 'umbrellas'
        expected = [
            'Bumbrellas', 'Cumbrellas', 'Dumbrellas', 'Fumbrellas',
            'Gumbrellas', 'Humbrellas', 'Jumbrellas', 'Kumbrellas',
            'Lumbrellas', 'Mumbrellas', 'Numbrellas', 'Pumbrellas',
            'Qumbrellas', 'Rumbrellas', 'Sumbrellas', 'Tumbrellas',
            'Vumbrellas', 'Wumbrellas', 'Xumbrellas', 'Yumbrellas',
            'Zumbrellas']
        self.assertEqual(techniques.all_prefix_first_vowel(word), expected)


class RecycleTestCase(unittest.TestCase):

    def test_pig_latinize(self):
        words = techniques.pig_latinize(['purring', 'cats'])
        self.assertEqual(techniques.recycle(
            words, techniques.pig_latinize),
            ['urringpaywayway', 'atscaywayway'])

    def test_portmanteau(self):
        words = ['ratchet', 'broccoli', 'potato', 'gadget', 'celery', 'hammer']
        res = techniques.recycle(
            words, techniques.make_portmanteau_default_vowel)
        expected = ['potatchelery', 'potatchelery', 'potadgelery',
                    'potadgelery', 'potammelery', 'potammelery',
                    'ratchelery', 'ratchelery']
        self.assertEqual(res, expected)


class SuperScrubTestCase(unittest.TestCase):

    def test_uniq(self):
        data = {'words': {'technique': ['words', 'words']}}
        self.assertEqual(
            techniques.super_scrub(data)['words']['technique'], ['words'])

    def test_remove_odd(self):
        data = {'words': {'technique': ['asdsaasdokokk', 'words']}}
        self.assertEqual(
            techniques.super_scrub(data)['words']['technique'], ['words'])

    def test_cleansort(self):
        data = {'words': {'technique': ['!!@words', 'radio0']}}
        self.assertEqual(
            techniques.super_scrub(data)['words']['technique'],
            ['radio', 'words'])


class BackronymTestCase(unittest.TestCase):

    def test_basic(self):
        res = techniques.backronym('rad', 'computer', max_attempts=5)
        self.assertIsInstance(res, dict)
        expected_keys = ['acronym', 'backronym', 'words',
                         'success_ratio', 'success']
        for key in expected_keys:
            self.assertTrue(key in res)
