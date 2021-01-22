''' quiz.py: Quiz class '''

import itertools
import os
import yaml

# Dredd Quiz Class ------------------------------------------------------------

class Quiz(object):
    ''' Dredd Quiz Class '''

    def __init__(self, quiz_path):
        questions_path = os.path.join(quiz_path, 'questions.yaml')
        answers_path   = os.path.join(quiz_path, 'answers.yaml')

        with open(questions_path) as questions_stream:
            self.questions = yaml.safe_load(questions_stream)

        with open(answers_path) as answers_stream:
            self.answers   = yaml.safe_load(answers_stream)

    def evaluate(self, responses):
        ''' Evaluate Quiz responses '''
        result = {}
        points = {}
        for question, response in responses.items():
            try:
                if self.questions[question]['type'] == 'single':
                    result[question], points[question] = self.evaluate_single(question, response)
                elif self.questions[question]['type'] == 'multiple':
                    result[question], points[question] = self.evaluate_multiple(question, response)
                elif self.questions[question]['type'] == 'order':
                    result[question], points[question] = self.evaluate_order(question, response)
                elif self.questions[question]['type'] == 'blank':
                    result[question], points[question] = self.evaluate_blank(question, response)
                else:
                    result[question], points[question] = 0, 0
            except KeyError:
                result[question], points[question] = 0, 0

        result['score']  = float('{:0.4f}'.format(sum(result.values())))
        result['value']  = float('{:0.4f}'.format(sum(points.values())))
        result['status'] = 0 if len(responses) == len(self.answers) and result['score'] >= result['value'] else 1
        return result

    def evaluate_single(self, question, response):
        values = []
        for answer, value in self.answers[question]:
            values.append(value)
            if response == answer:
                return value, max(values)
        return 0, max(values)

    def evaluate_multiple(self, question, responses):
        if isinstance(responses, str):
            responses = [responses]

        answers, value = self.answers[question]
        rset    = set(responses)
        aset    = set(answers)
        missing = 1.0*len(aset.difference(rset)) / len(answers)
        extra   = 0.5*len(rset.difference(aset)) / len(answers)
        return (1.0 - missing - extra)*value, value

    def evaluate_order(self, question, responses):
        answers, value = self.answers[question]
        ratio = sum(1 for r, a in zip(responses, answers) if r == a) / len(answers)
        return ratio * value, value

    def evaluate_blank(self, question, responses):
        result = 0
        points = 0

        if isinstance(responses, str):
            responses = [responses]

        for response, answers in zip(responses, self.answers[question]):
            values = []
            for answer, value in answers:
                values.append(value)
                if answer.lower() == response.lower():
                    result += value
                    break
            points += max(values)
        return result, points

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
