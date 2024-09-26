import unittest

from wilhelm_python_sdk.ancient_greek_wiktionary_parser import \
    parse_all_conjugation_tables


class TestNeo4jLoader(unittest.TestCase):

    def test_parse_all_conjugation_tables(self):
        tables = parse_all_conjugation_tables("https://en.wiktionary.org/wiki/ἔχω")

        self.assertEqual(
            [
                ['number', 'number', 'singular', 'singular', 'singular', 'dual', 'dual', 'plural', 'plural', 'plural'],
                ['', '', 'first', 'second', 'third', 'second', 'third', 'first', 'second', 'third'],
                ['active', 'indicative', 'ἔχω', 'ἔχεις', 'ἔχει', 'ἔχετον', 'ἔχετον', 'ἔχομεν', 'ἔχετε', 'ἔχουσῐ(ν)'],
                ['active', 'subjunctive', 'ἔχω', 'ἔχῃς', 'ἔχῃ', 'ἔχητον', 'ἔχητον', 'ἔχωμεν', 'ἔχητε', 'ἔχωσῐ(ν)'],
                ['active', 'optative', 'ἔχοιμῐ', 'ἔχοις', 'ἔχοι', 'ἔχοιτον', 'ἐχοίτην', 'ἔχοιμεν', 'ἔχοιτε', 'ἔχοιεν'],
                ['active', 'imperative', '', 'ἔχε', 'ἐχέτω', 'ἔχετον', 'ἐχέτων', '', 'ἔχετε', 'ἐχόντων'],
                ['middle/passive', 'indicative', 'ἔχομαι', 'ἔχῃ,ἔχει', 'ἔχεται', 'ἔχεσθον', 'ἔχεσθον', 'ἐχόμεθᾰ',
                 'ἔχεσθε', 'ἔχονται'],
                ['middle/passive', 'subjunctive', 'ἔχωμαι', 'ἔχῃ', 'ἔχηται', 'ἔχησθον', 'ἔχησθον', 'ἐχώμεθᾰ', 'ἔχησθε',
                 'ἔχωνται'],
                ['middle/passive', 'optative', 'ἐχοίμην', 'ἔχοιο', 'ἔχοιτο', 'ἔχοισθον', 'ἐχοίσθην', 'ἐχοίμεθᾰ',
                 'ἔχοισθε', 'ἔχοιντο'],
                ['middle/passive', 'imperative', '', 'ἔχου', 'ἐχέσθω', 'ἔχεσθον', 'ἐχέσθων', '', 'ἔχεσθε', 'ἐχέσθων'],
                ['', '', 'active', 'active', 'active', 'active', 'middle/passive', 'middle/passive', 'middle/passive',
                 'middle/passive'],
                ['infinitive', 'infinitive', 'ἔχειν', 'ἔχειν', 'ἔχειν', 'ἔχειν', 'ἔχεσθαι', 'ἔχεσθαι', 'ἔχεσθαι',
                 'ἔχεσθαι'],
                ['participle', 'm', 'ἔχων', 'ἔχων', 'ἔχων', 'ἔχων', 'ἐχόμενος', 'ἐχόμενος', 'ἐχόμενος', 'ἐχόμενος'],
                ['participle', 'f', 'ἔχουσᾰ', 'ἔχουσᾰ', 'ἔχουσᾰ', 'ἔχουσᾰ', 'ἐχομένη', 'ἐχομένη', 'ἐχομένη', 'ἐχομένη'],
                ['participle', 'n', 'ἔχον', 'ἔχον', 'ἔχον', 'ἔχον', 'ἐχόμενον', 'ἐχόμενον', 'ἐχόμενον', 'ἐχόμενον']
            ],
            tables["Present: ἔχω, ἔχομαι"]
        )
