from unittest.mock import patch
from unittest import TestCase, main
import computer


def get_input(text):
    return input(text)


def forTest():
    inp = str(get_input("> "))
    if inp == 'quit()':
        return True
    else:
        return computer.getData(inp)

class MyTestCase(TestCase):

    # Test quit()
    @patch('computerTest.get_input', return_value='quit()')
    def test_answer_yes(self, input):
        self.assertEqual(forTest(), True)

    # Test first part variable
    @patch('computerTest.get_input', return_value='a = 5')
    def test_first_part_var(self, input):
        self.assertEqual(forTest(), {'variable': 'a', 'sign': '+'})

    # Test first part function
    @patch('computerTest.get_input', return_value='funcA(x) = 5')
    def test_first_part_func(self, input):
        self.assertEqual(forTest(), {'function': {'name': 'funcA', 'variable': 'x', 'sign': '+'}, 'sign': '+'})

    @patch('computerTest.get_input', return_value='5 = 5')
    def test_first_part_number(self, input):
        result = \
            {'number': 5, 'sign': '+'}
        self.assertEqual(forTest(), result)

    @patch('computerTest.get_input', return_value='(5 + 3) = 5')
    def test_first_part_number2(self, input):
        result = \
            {
                'number': 8,
                'sign': '+'
            }
        self.assertEqual(forTest(), result)

    # Test first part operation
    @patch('computerTest.get_input', return_value='a + 5 = 5')
    def test_first_part_operation(self, input):
        result = {
            'operation': [
                {
                    'sign': '+',
                    'variable': 'a'
                },
                {
                    'sign': '+',
                    'number': 5
                 }
            ],
            'sign': '+'
        }
        self.assertEqual(forTest(), result)

    @patch('computerTest.get_input', return_value='(a + 5) + 3 = 5')
    def test_first_part_operation2(self, input):
        result = \
            {
                'operation':
                    [
                        {
                            'parenthesis':
                                [
                                    {
                                        'sign': '+',
                                        'variable': 'a'
                                    },
                                    {
                                        'number': 5,
                                        'sign': '+'
                                    }
                                ],
                            'sign': '+'
                        },
                    {
                        'number': 3,
                        'sign': '+'
                    }
                ],
                'sign': '+'
            }
        self.assertEqual(forTest(), result)

    @patch('computerTest.get_input', return_value='(a + 5) * (3 - x) = 5')
    def test_first_part_operation3(self, input):
        result = \
            {
                'operation':
                    [
                        {
                            'parenthesis':
                                [
                                    {
                                        'sign': '+',
                                        'variable': 'a'
                                    },
                                    {
                                        'number': 5,
                                        'sign': '+'
                                    }
                                ],
                            'sign': '+'
                        },
                        {
                            'parenthesis':
                                [
                                    {
                                        'sign': '+',
                                        'number': 3
                                    },
                                    {
                                        'variable': 'x',
                                        'sign': '-'
                                    }
                                ],
                            'sign': '*'
                        },
                ],
                'sign': '+'
            }
        self.assertEqual(forTest(), result)

    @patch('computerTest.get_input', return_value='(a + 5) * (3 - x) +(x)= 5')
    def test_first_part_operation4(self, input):
        result = \
            {
                'operation':
                    [
                        {
                            'parenthesis':
                                [
                                    {
                                        'sign': '+',
                                        'variable': 'a'
                                    },
                                    {
                                        'number': 5,
                                        'sign': '+'
                                    }
                                ],
                            'sign': '+'
                        },
                        {
                            'parenthesis':
                                [
                                    {
                                        'sign': '+',
                                        'number': 3
                                    },
                                    {
                                        'variable': 'x',
                                        'sign': '-'
                                    }
                                ],
                            'sign': '*'
                        },
                        {
                            'variable': 'x',
                            'sign': '+'
                        }
                ],
                'sign': '+'
            }
        self.assertEqual(forTest(), result)

    @patch('computerTest.get_input', return_value='(a + 5) * (3 - x) + funcA(x)= 5')
    def test_first_part_operation5(self, input):
        result = \
            {
                'operation':
                    [
                        {
                            'parenthesis':
                                [
                                    {
                                        'sign': '+',
                                        'variable': 'a'
                                    },
                                    {
                                        'number': 5,
                                        'sign': '+'
                                    }
                                ],
                            'sign': '+'
                        },
                        {
                            'parenthesis':
                                [
                                    {
                                        'sign': '+',
                                        'number': 3
                                    },
                                    {
                                        'variable': 'x',
                                        'sign': '-'
                                    }
                                ],
                            'sign': '*'
                        },
                        {
                            'function': 'funcA(x)',
                            'sign': '+'
                        }
                    ],
                'sign': '+'
            }
        self.assertEqual(forTest(), result)

    @patch('computerTest.get_input', return_value='(a + 5) * (4 / (3 - x)) = 5')
    def test_first_part_operation6(self, input):
        result = \
            {'operation':
                 [
                     {'parenthesis': [{'variable': 'a', 'sign': '+'}, {'number': 5, 'sign': '+'}],
                      'sign': '+'},

                     {'parenthesis': [
                         {'number': 4, 'sign': '+'},
                         {'parenthesis': [
                            {'number': 3, 'sign': '+'},
                            {'variable': 'x', 'sign': '-'}],
                         'sign': '/'}],
                     'sign': '*'}
                 ],
                'sign': '+'
            }

        self.assertEqual(forTest(), result)

    @patch('computerTest.get_input', return_value='(a + 5) = 5')
    def test_first_part_operation7(self, input):
        result = \
            {
                'operation': [
                    {'sign': '+',
                    'parenthesis': [
                        {'variable': 'a', 'sign': '+'},
                        {'number': 5, 'sign': '+'}
                    ]}
                ],
                'sign': '+'
            }

        self.assertEqual(forTest(), result)


    @patch('computerTest.get_input', return_value='funcA(a + 5) * (4 / (3 - x)) = 5')
    def test_first_part_function(self, input):
        result = {'operation':
                      [
                          {'sign': '+', 'function': {'name': 'funcA', 'sign': '+', 'operation': [
                              {'sign': '+', 'variable': 'a'}, {'sign': '+', 'number': 5}]}},
                          {'sign': '*', 'parenthesis': [
                              {'sign': '+', 'number': 4},
                              {'sign': '/', 'parenthesis': [
                                  {'sign': '+', 'number': 3},
                                  {'sign': '-', 'variable': 'x'}
                              ]}]}
                      ],
                'sign': '+'
        }

        self.assertEqual(forTest(), result)

    @patch('computerTest.get_input', return_value='funcA(5) = 3')
    def test_first_part_function2(self, input):
        result = {
            'operation': [{
                'function': {
                    'number': 5,
                    'sign': '+',
                    'name': 'funcA'},
                "sign": '+'}
            ],
            'sign': '+'
        }

        self.assertEqual(forTest(), result)

if __name__ == '__main__':
    main()



