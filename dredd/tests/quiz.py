#!/usr/bin/env python2.7

''' dredd.test.quiz: Test Quiz class '''

import os
import sys
import unittest

sys.path.append(os.curdir)

import dredd.quiz


class QuizSingleTestCase(unittest.TestCase):
    ''' Dredd Quiz Single Choice Test Case '''

    def test_00_single_load(self):
        quiz = dredd.quiz.Quiz('data/quiz/test-single')

        self.assertTrue(len(quiz.questions) == 2)
        self.assertTrue(len(quiz.answers)   == 2)

    def test_01_single_q1(self):
        quiz = dredd.quiz.Quiz('data/quiz/test-single')

        result = quiz.evaluate({'q1': 'blue'})
        self.assertTrue(result['q1'] == 0.5)
        self.assertTrue(result['total'] == 0.5)

        result = quiz.evaluate({'q1': 'green'})
        self.assertTrue(result['q1'] == 0.25)
        self.assertTrue(result['total'] == 0.25)

        result = quiz.evaluate({'q1': 'red'})
        self.assertTrue(result['q1'] == 0.0)
        self.assertTrue(result['total'] == 0.0)

        result = quiz.evaluate({'q1': 'purple'})
        self.assertTrue(result['q1'] == 0.0)
        self.assertTrue(result['total'] == 0.0)

    def test_02_single_q2(self):
        quiz = dredd.quiz.Quiz('data/quiz/test-single')

        result = quiz.evaluate({'q2': True})
        self.assertTrue(result['q2'] == 0.5)
        self.assertTrue(result['total'] == 0.5)

        result = quiz.evaluate({'q2': False})
        self.assertTrue(result['q2'] == 0.0)
        self.assertTrue(result['total'] == 0.0)

        result = quiz.evaluate({'q2': None})
        self.assertTrue(result['q2'] == 0.0)
        self.assertTrue(result['total'] == 0.0)

    def test_03_single_total(self):
        quiz = dredd.quiz.Quiz('data/quiz/test-single')

        result = quiz.evaluate({'q1': 'blue', 'q2': True})
        self.assertTrue(result['total'] == 1.0)

        result = quiz.evaluate({'q1': 'blue', 'q2': False})
        self.assertTrue(result['total'] == 0.5)

        result = quiz.evaluate({'q1': 'green', 'q2': False})
        self.assertTrue(result['total'] == 0.25)

        result = quiz.evaluate({'q1': 'green', 'q2': True})
        self.assertTrue(result['total'] == 0.75)

        result = quiz.evaluate({'q1': 'red', 'q2': True})
        self.assertTrue(result['total'] == 0.5)

        result = quiz.evaluate({'q1': 'red', 'q2': False})
        self.assertTrue(result['total'] == 0.0)


class QuizMultipleTestCase(unittest.TestCase):
    ''' Dredd Quiz Multiple Choice Test Case '''

    def test_00_multiple_load(self):
        quiz = dredd.quiz.Quiz('data/quiz/test-multiple')

        self.assertTrue(len(quiz.questions) == 2)
        self.assertTrue(len(quiz.answers)   == 2)

    def test_01_multiple_q1(self):
        quiz = dredd.quiz.Quiz('data/quiz/test-multiple')

        result = quiz.evaluate({'q1': ['blue']})
        self.assertTrue(result['q1'] == 0.25)
        self.assertTrue(result['total'] == 0.25)

        result = quiz.evaluate({'q1': ['blue', 'green']})
        self.assertTrue(result['q1'] == 0.5)
        self.assertTrue(result['total'] == 0.5)

        result = quiz.evaluate({'q1': ['green']})
        self.assertTrue(result['q1'] == 0.25)
        self.assertTrue(result['total'] == 0.25)

        result = quiz.evaluate({'q1': ['red']})
        self.assertTrue(result['q1'] == 0.0)
        self.assertTrue(result['total'] == 0.0)

        result = quiz.evaluate({'q1': ['red', 'blue']})
        self.assertTrue(result['q1'] == 0.25)
        self.assertTrue(result['total'] == 0.25)

    def test_02_multiple_q2(self):
        quiz = dredd.quiz.Quiz('data/quiz/test-multiple')

        result = quiz.evaluate({'q2': ['pizza']})
        self.assertTrue(result['q2'] == 0.25)
        self.assertTrue(result['total'] == 0.25)

        result = quiz.evaluate({'q2': ['pizza', 'tacos']})
        self.assertTrue(result['q2'] == 0.5)
        self.assertTrue(result['total'] == 0.5)

        result = quiz.evaluate({'q2': ['tacos']})
        self.assertTrue(result['q2'] == 0.25)
        self.assertTrue(result['total'] == 0.25)

        result = quiz.evaluate({'q2': ['burger']})
        self.assertTrue(result['q2'] == 0.0)
        self.assertTrue(result['total'] == 0.0)

        result = quiz.evaluate({'q2': ['burger', 'tacos']})
        self.assertTrue(result['q2'] == 0.25)
        self.assertTrue(result['total'] == 0.25)

    def test_03_multiple_total(self):
        quiz = dredd.quiz.Quiz('data/quiz/test-multiple')

        result = quiz.evaluate({'q1': ['blue'], 'q2': ['pizza']})
        self.assertTrue(result['total'] == 0.5)

        result = quiz.evaluate({'q1': ['green'], 'q2': ['pizza']})
        self.assertTrue(result['total'] == 0.5)

        result = quiz.evaluate({'q1': ['blue', 'green'], 'q2': ['pizza']})
        self.assertTrue(result['total'] == 0.75)

        result = quiz.evaluate({'q1': ['blue', 'green'], 'q2': ['pizza', 'tacos']})
        self.assertTrue(result['total'] == 1.00)

        result = quiz.evaluate({'q1': ['blue', 'green'], 'q2': ['pizza', 'burger']})
        self.assertTrue(result['total'] == 0.75)

        result = quiz.evaluate({'q1': ['red'], 'q2': ['pizza', 'burger']})
        self.assertTrue(result['total'] == 0.25)


class QuizOrderTestCase(unittest.TestCase):
    ''' Dredd Quiz Ordered List Test Case '''

    def test_00_order_load(self):
        quiz = dredd.quiz.Quiz('data/quiz/test-order')

        self.assertTrue(len(quiz.questions) == 2)
        self.assertTrue(len(quiz.answers)   == 2)

    def test_01_order_q1(self):
        quiz = dredd.quiz.Quiz('data/quiz/test-order')

        result = quiz.evaluate({'q1': ['blue', 'green', 'red']})
        self.assertTrue(result['q1'] == 0.5)
        self.assertTrue(result['total'] == 0.5)

        result = quiz.evaluate({'q1': ['blue', 'red', 'green']})
        self.assertTrue(result['q1'] == 1/3.0)
        self.assertTrue(result['total'] == 1/3.0)

        result = quiz.evaluate({'q1': ['blue', 'green']})
        self.assertTrue(result['q1'] == 0.4)
        self.assertTrue(result['total'] == 0.4)

        result = quiz.evaluate({'q1': ['blue', 'orange', 'red']})
        self.assertTrue(result['q1'] == 1/3.0)
        self.assertTrue(result['total'] == 1/3.0)

        result = quiz.evaluate({'q1': ['blue']})
        self.assertTrue(result['q1'] == 0.25)
        self.assertTrue(result['total'] == 0.25)

        result = quiz.evaluate({'q1': []})
        self.assertTrue(result['q1'] == 0)
        self.assertTrue(result['total'] == 0)

    def test_02_order_q2(self):
        quiz = dredd.quiz.Quiz('data/quiz/test-order')

        result = quiz.evaluate({'q2': ['tacos', 'burgers', 'pizza', 'salads']})
        self.assertTrue(result['q2'] == 0.5)
        self.assertTrue(result['total'] == 0.5)

        result = quiz.evaluate({'q2': ['tacos', 'burgers', 'salads']})
        self.assertTrue(result['q2'] <= 0.43)
        self.assertTrue(result['total'] <= 0.43)

        result = quiz.evaluate({'q2': ['tacos', 'burgers', 'salads', 'pizza']})
        self.assertTrue(result['q2'] == 0.375)
        self.assertTrue(result['total'] <= 0.375)

        result = quiz.evaluate({'q2': []})
        self.assertTrue(result['q2'] == 0)
        self.assertTrue(result['total'] == 0)

    def test_03_order_total(self):
        quiz = dredd.quiz.Quiz('data/quiz/test-order')

        result = quiz.evaluate({
            'q1': ['blue', 'green', 'red'],
            'q2': ['tacos', 'burgers', 'pizza', 'salads']
        })
        self.assertTrue(result['total'] == 1.0)

        result = quiz.evaluate({
            'q1': ['blue', 'green', 'red'],
            'q2': []
        })
        self.assertTrue(result['total'] == 0.5)

        result = quiz.evaluate({
            'q1': [],
            'q2': ['tacos', 'burgers', 'pizza', 'salads']
        })
        self.assertTrue(result['total'] == 0.5)


class QuizBlankTestCase(unittest.TestCase):
    ''' Dredd Quiz Fill-In-The Blank Test Case '''

    def test_00_blank_load(self):
        quiz = dredd.quiz.Quiz('data/quiz/test-blank')

        self.assertTrue(len(quiz.questions) == 2)
        self.assertTrue(len(quiz.answers)   == 2)

    def test_01_order_q1(self):
        quiz = dredd.quiz.Quiz('data/quiz/test-blank')

        result = quiz.evaluate({'q1': ['came', 'saw', 'conquered']})
        self.assertTrue(result['q1'] == 0.75)
        self.assertTrue(result['total'] == 0.75)

        result = quiz.evaluate({'q1': ['come', 'saw', 'conquered']})
        self.assertTrue(result['q1'] == 0.75)

        result = quiz.evaluate({'q1': ['come', 'saw']})
        self.assertTrue(result['q1'] == 0.5)
        self.assertTrue(result['total'] == 0.5)

        result = quiz.evaluate({'q1': ['come']})
        self.assertTrue(result['q1'] == 0.25)
        self.assertTrue(result['total'] == 0.25)

        result = quiz.evaluate({'q1': []})
        self.assertTrue(result['q1'] == 0.0)
        self.assertTrue(result['total'] == 0.0)

        result = quiz.evaluate({'q1': ['come', 'see', 'derp']})
        self.assertTrue(result['q1'] == 0.5)
        self.assertTrue(result['total'] == 0.5)

    def test_02_order_q2(self):
        quiz = dredd.quiz.Quiz('data/quiz/test-blank')

        result = quiz.evaluate({'q2': ['batman']})
        self.assertTrue(result['q2'] == 0.5)
        self.assertTrue(result['total'] == 0.5)

        result = quiz.evaluate({'q2': ['many']})
        self.assertTrue(result['q2'] == 0.0)
        self.assertTrue(result['total'] == 0.0)

        result = quiz.evaluate({'q2': ['IRONMAN']})
        self.assertTrue(result['q2'] == 0.5)
        self.assertTrue(result['total'] == 0.5)

        result = quiz.evaluate({'q2': ['deadpool']})
        self.assertTrue(result['q2'] == 0.5)
        self.assertTrue(result['total'] == 0.5)

        result = quiz.evaluate({'q2': ['D34dP001']})
        self.assertTrue(result['q2'] == 0.5)
        self.assertTrue(result['total'] == 0.5)

        result = quiz.evaluate({'q2': ['deadpooll']})
        self.assertTrue(result['q2'] == 0.0)
        self.assertTrue(result['total'] == 0.0)

    def test_03_order_total(self):
        quiz = dredd.quiz.Quiz('data/quiz/test-blank')

        result = quiz.evaluate({
            'q1': ['came', 'saw', 'conquered'],
            'q2': ['batman']
        })
        self.assertTrue(result['total'] == 1.25)

        result = quiz.evaluate({
            'q1': ['came', 'derp', 'conquered'],
            'q2': ['batman']
        })
        self.assertTrue(result['total'] == 1.00)

        result = quiz.evaluate({
            'q1': ['came', 'derp'],
            'q2': ['batman']
        })
        self.assertTrue(result['total'] == 0.75)

        result = quiz.evaluate({
            'q1': ['came', 'derp'],
            'q2': ['batmany']
        })
        self.assertTrue(result['total'] == 0.25)


if __name__ == '__main__':
    unittest.main()

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
