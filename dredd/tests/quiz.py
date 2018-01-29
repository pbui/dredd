#!/usr/bin/env python2.7

''' dredd.test.quiz: Test Quiz class '''

import os
import sys
import unittest

sys.path.append(os.curdir)

import dredd.quiz

# Dredd Quiz Single Choice Test Case ------------------------------------------

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
        self.assertTrue(result['score'] == 0.5)

        result = quiz.evaluate({'q1': 'green'})
        self.assertTrue(result['q1'] == 0.25)
        self.assertTrue(result['score'] == 0.25)

        result = quiz.evaluate({'q1': 'red'})
        self.assertTrue(result['q1'] == 0.0)
        self.assertTrue(result['score'] == 0.0)

        result = quiz.evaluate({'q1': 'purple'})
        self.assertTrue(result['q1'] == 0.0)
        self.assertTrue(result['score'] == 0.0)

    def test_02_single_q2(self):
        quiz = dredd.quiz.Quiz('data/quiz/test-single')

        result = quiz.evaluate({'q2': True})
        self.assertTrue(result['q2'] == 0.5)
        self.assertTrue(result['score'] == 0.5)

        result = quiz.evaluate({'q2': False})
        self.assertTrue(result['q2'] == 0.0)
        self.assertTrue(result['score'] == 0.0)

        result = quiz.evaluate({'q2': None})
        self.assertTrue(result['q2'] == 0.0)
        self.assertTrue(result['score'] == 0.0)

    def test_03_single_score(self):
        quiz = dredd.quiz.Quiz('data/quiz/test-single')

        result = quiz.evaluate({'q1': 'blue', 'q2': True})
        self.assertTrue(result['score'] == 1.0)

        result = quiz.evaluate({'q1': 'blue', 'q2': False})
        self.assertTrue(result['score'] == 0.5)

        result = quiz.evaluate({'q1': 'green', 'q2': False})
        self.assertTrue(result['score'] == 0.25)

        result = quiz.evaluate({'q1': 'green', 'q2': True})
        self.assertTrue(result['score'] == 0.75)

        result = quiz.evaluate({'q1': 'red', 'q2': True})
        self.assertTrue(result['score'] == 0.5)

        result = quiz.evaluate({'q1': 'red', 'q2': False})
        self.assertTrue(result['score'] == 0.0)

# Dredd Quiz Multiple Choice Test Case -----------------------------------------

class QuizMultipleTestCase(unittest.TestCase):
    ''' Dredd Quiz Multiple Choice Test Case '''

    def test_00_multiple_load(self):
        quiz = dredd.quiz.Quiz('data/quiz/test-multiple')

        self.assertTrue(len(quiz.questions) == 2)
        self.assertTrue(len(quiz.answers)   == 2)

    def test_01_multiple_q1(self):
        quiz = dredd.quiz.Quiz('data/quiz/test-multiple')

        result = quiz.evaluate({'q1': ['blue']})
        self.assertTrue(result['q1'] == 1/3.0)
        self.assertTrue(abs(result['score'] - 1/3.0) < 0.0001)

        result = quiz.evaluate({'q1': ['blue', 'green']})
        self.assertTrue(result['q1'] == 0.5)
        self.assertTrue(result['score'] == 0.5)

        result = quiz.evaluate({'q1': ['green']})
        self.assertTrue(result['q1'] == 1/3.0)
        self.assertTrue(abs(result['score'] - 1/3.0) < 0.0001)

        result = quiz.evaluate({'q1': ['red']})
        self.assertTrue(result['q1'] == 0.0)
        self.assertTrue(result['score'] == 0.0)

        result = quiz.evaluate({'q1': ['red', 'blue']})
        self.assertTrue(result['q1'] == 0.25)
        self.assertTrue(result['score'] == 0.25)

        result = quiz.evaluate({'q1': ['red', 'blue', 'green']})
        self.assertTrue(result['q1'] == 0.4)
        self.assertTrue(result['score'] == 0.4)

    def test_02_multiple_q2(self):
        quiz = dredd.quiz.Quiz('data/quiz/test-multiple')

        result = quiz.evaluate({'q2': ['pizza']})
        self.assertTrue(result['q2'] == 1/3.0)
        self.assertTrue(abs(result['score'] - 1/3.0) < 0.0001)

        result = quiz.evaluate({'q2': ['pizza', 'tacos']})
        self.assertTrue(result['q2'] == 0.5)
        self.assertTrue(result['score'] == 0.5)

        result = quiz.evaluate({'q2': ['tacos']})
        self.assertTrue(result['q2'] == 1/3.0)
        self.assertTrue(abs(result['score'] - 1/3.0) < 0.0001)

        result = quiz.evaluate({'q2': ['burger']})
        self.assertTrue(result['q2'] == 0.0)
        self.assertTrue(result['score'] == 0.0)

        result = quiz.evaluate({'q2': ['burger', 'tacos']})
        self.assertTrue(result['q2'] == 0.25)
        self.assertTrue(result['score'] == 0.25)

    def test_03_multiple_score(self):
        quiz = dredd.quiz.Quiz('data/quiz/test-multiple')

        result = quiz.evaluate({'q1': 'blue', 'q2': 'pizza'})
        self.assertTrue(abs(result['score'] - 2/3.0) < 0.0001)

        result = quiz.evaluate({'q1': ['green'], 'q2': ['pizza']})
        self.assertTrue(abs(result['score'] - 2/3.0) < 0.0001)

        result = quiz.evaluate({'q1': ['blue', 'green'], 'q2': ['pizza']})
        self.assertTrue(abs(result['score'] - (0.5 + 1/3.0)) < 0.0001)

        result = quiz.evaluate({'q1': ['blue', 'green'], 'q2': ['pizza', 'tacos']})
        self.assertTrue(result['score'] == 1.00)

        result = quiz.evaluate({'q1': ['blue', 'green'], 'q2': ['pizza', 'burger']})
        self.assertTrue(result['score'] == 0.75)

        result = quiz.evaluate({'q1': ['red'], 'q2': ['pizza', 'burger']})
        self.assertTrue(result['score'] == 0.25)

        result = quiz.evaluate({'q1': ['red', 'blue', 'green'], 'q2': ['pizza', 'burger']})
        self.assertTrue(result['score'] == 0.65)

# Dredd Quiz Ordered List Test Case --------------------------------------------

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
        self.assertTrue(result['score'] == 0.5)

        result = quiz.evaluate({'q1': ['blue', 'red', 'green']})
        self.assertTrue(result['q1'] == 1/3.0)
        self.assertTrue(abs(result['score'] - 1/3.0) < 0.0001)

        result = quiz.evaluate({'q1': ['blue', 'green']})
        self.assertTrue(result['q1'] == 0.4)
        self.assertTrue(result['score'] == 0.4)

        result = quiz.evaluate({'q1': ['blue', 'orange', 'red']})
        self.assertTrue(result['q1'] == 1/3.0)
        self.assertTrue(abs(result['score'] - 1/3.0) < 0.0001)

        result = quiz.evaluate({'q1': ['blue']})
        self.assertTrue(result['q1'] == 0.25)
        self.assertTrue(result['score'] == 0.25)

        result = quiz.evaluate({'q1': []})
        self.assertTrue(result['q1'] == 0)
        self.assertTrue(result['score'] == 0)

    def test_02_order_q2(self):
        quiz = dredd.quiz.Quiz('data/quiz/test-order')

        result = quiz.evaluate({'q2': ['tacos', 'burgers', 'pizza', 'salads']})
        self.assertTrue(result['q2'] == 0.5)
        self.assertTrue(result['score'] == 0.5)

        result = quiz.evaluate({'q2': ['tacos', 'burgers', 'salads']})
        self.assertTrue(result['q2'] <= 0.43)
        self.assertTrue(result['score'] <= 0.43)

        result = quiz.evaluate({'q2': ['tacos', 'burgers', 'salads', 'pizza']})
        self.assertTrue(result['q2'] == 0.375)
        self.assertTrue(result['score'] <= 0.375)

        result = quiz.evaluate({'q2': []})
        self.assertTrue(result['q2'] == 0)
        self.assertTrue(result['score'] == 0)

    def test_03_order_score(self):
        quiz = dredd.quiz.Quiz('data/quiz/test-order')

        result = quiz.evaluate({
            'q1': ['blue', 'green', 'red'],
            'q2': ['tacos', 'burgers', 'pizza', 'salads']
        })
        self.assertTrue(result['score'] == 1.0)

        result = quiz.evaluate({
            'q1': ['blue', 'green', 'red'],
            'q2': []
        })
        self.assertTrue(result['score'] == 0.5)

        result = quiz.evaluate({
            'q1': [],
            'q2': ['tacos', 'burgers', 'pizza', 'salads']
        })
        self.assertTrue(result['score'] == 0.5)

# Dredd Quiz Fill-In-The-Blank Test Case --------------------------------------

class QuizBlankTestCase(unittest.TestCase):
    ''' Dredd Quiz Fill-In-The Blank Test Case '''

    def test_00_blank_load(self):
        quiz = dredd.quiz.Quiz('data/quiz/test-blank')

        self.assertTrue(len(quiz.questions) == 1)
        self.assertTrue(len(quiz.answers)   == 1)

    def test_01_blank_q1(self):
        quiz = dredd.quiz.Quiz('data/quiz/test-blank')

        result = quiz.evaluate({'q1': ['came', 'saw', 'conquered']})
        self.assertTrue(result['q1'] == 0.75)
        self.assertTrue(result['score'] == 0.75)

        result = quiz.evaluate({'q1': ['come', 'saw', 'conquered']})
        self.assertTrue(result['q1'] == 0.75)

        result = quiz.evaluate({'q1': ['come', 'saw']})
        self.assertTrue(result['q1'] == 0.5)
        self.assertTrue(result['score'] == 0.5)

        result = quiz.evaluate({'q1': ['come']})
        self.assertTrue(result['q1'] == 0.25)
        self.assertTrue(result['score'] == 0.25)

        result = quiz.evaluate({'q1': []})
        self.assertTrue(result['q1'] == 0.0)
        self.assertTrue(result['score'] == 0.0)

        result = quiz.evaluate({'q1': ['come', 'see', 'derp']})
        self.assertTrue(result['q1'] == 0.5)
        self.assertTrue(result['score'] == 0.5)

    def test_02_blank_score(self):
        quiz = dredd.quiz.Quiz('data/quiz/test-blank')

        result = quiz.evaluate({
            'q1': ['came', 'saw', 'conquered'],
        })
        self.assertTrue(result['score'] == 0.75)

        result = quiz.evaluate({
            'q1': ['came', 'derp', 'conquered'],
        })
        self.assertTrue(result['score'] == 0.50)

        result = quiz.evaluate({
            'q1': ['came', 'derp'],
        })
        self.assertTrue(result['score'] == 0.25)

# Main Execution --------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
