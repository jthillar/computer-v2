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
        equation = forTest()
        equationPart1 = equation.first
        equationPart2 = equation.second
        self.assertEqual(equationPart1, {'variable': 'a', 'sign': '+', 'coefficient': '1'})
        self.assertEqual(equationPart2, {'number': 5, 'sign': '+', 'coefficient': '1', 'resolution': False})

    # Test first part function
    @patch('computerTest.get_input', return_value='funcA(x) = 5')
    def test_first_part_func(self, input):

        equation = forTest()
        equationPart1 = equation.first
        equationPart2 = equation.second
        self.assertEqual(equationPart1, {
            'function': {
                'name': 'funcA',
                'variable': 'x',
                'coefficient': '1',
                'sign': '+'},
            'coefficient': '1',
            'sign': '+'
        })
        self.assertEqual(equationPart2, {
            'number': 5,
            'coefficient': '1',
            'sign': '+',
            'resolution': False
        })

    @patch('computerTest.get_input', return_value='5 = 5')
    def test_first_part_number(self, input):

        equation = forTest()
        equationPart1 = equation.first
        test1 = {'number': 5, 'coefficient': '1', 'sign': '+'}
        
        equationPart2 = equation.second
        test2 = {'number': 5, 'coefficient': '1', 'sign': '+', 'resolution': False}
        self.assertEqual(equationPart1, test1)
        self.assertEqual(equationPart2, test2)

    @patch('computerTest.get_input', return_value='(5 + 3) = 5')
    def test_first_part_number2(self, input):
        equation = forTest()
        equationPart1 = equation.first
        test1 = \
            {
                'number': 8,
                'sign': '+',
                'coefficient': '1',
            }
        equationPart2 = equation.second
        test2 = {'number': 5, 'coefficient': '1', 'sign': '+', 'resolution': False}
        self.assertEqual(equationPart1, test1)
        self.assertEqual(equationPart2, test2)


    @patch('computerTest.get_input', return_value='[[2, 3]; [1, 2]; [4, 5]] = 3')
    def test_first_part_matrice(self, input):
       
        equation = forTest()
        equationPart1 = equation.first
        equationPart2 = equation.second
        test1 = \
            {
                'matrice': [
                    [
                        {'number': 2, 'coefficient': '1', 'sign': '+'},
                        {'number': 3, 'coefficient': '1', 'sign': '+'},
                    ],
                    [
                        {'number': 1, 'coefficient': '1', 'sign': '+'},
                        {'number': 2, 'coefficient': '1', 'sign': '+'},
                    ],
                    [
                        {'number': 4, 'coefficient': '1', 'sign': '+'},
                        {'number': 5, 'coefficient': '1', 'sign': '+'},
                    ],

                ],
                'sign': '+',
                'coefficient': '1'
            }
        test2 = {'number': 3, 'coefficient': '1', 'sign': '+', 'resolution': False}

        self.assertEqual(equationPart1, test1)
        self.assertEqual(equationPart2, test2)

    # Test first part operation
    @patch('computerTest.get_input', return_value='a + 5 = 5')
    def test_first_part_operation(self, input):
        equation = forTest()
        equationPart1 = equation.first
        equationPart2 = equation.second
        test1 = {
            'coefficient': '1', 'sign': '+',
            'operation': [
                {
                    'sign': '+',
                    'coefficient': '1',
                    'variable': 'a'
                },
                {
                    'sign': '+',
                    'coefficient': '1',
                    'number': 5
                 }
            ],
        }
        test2 = {'number': 5, 'coefficient': '1', 'sign': '+', 'resolution': False}

        self.assertEqual(equationPart1, test1)
        self.assertEqual(equationPart2, test2)

    @patch('computerTest.get_input', return_value='(a + 5) + 3 = 5')
    def test_first_part_operation2(self, input):
        equation = forTest()
        equationPart1 = equation.first
        equationPart2 = equation.second
        test1 = \
            {
                'coefficient': '1', 'sign': '+',
                'operation':
                    [
                        {
                            'parenthesis':
                                [
                                    {
                                        'sign': '+',
                                        'coefficient': '1',
                                        'variable': 'a'
                                    },
                                    {
                                        'number': 5,
                                        'coefficient': '1',
                                        'sign': '+'
                                    }
                                ],
                            'coefficient': '1',
                            'sign': '+'
                        },
                    {
                        'number': 3,
                        'coefficient': '1',
                        'sign': '+'
                    }
                ],
            }
        test2 = {'number': 5, 'coefficient': '1', 'sign': '+', 'resolution': False}

        self.assertEqual(equationPart1, test1)
        self.assertEqual(equationPart2, test2)

    @patch('computerTest.get_input', return_value='(a + 5) * (3 - x) = 5')
    def test_first_part_operation3(self, input):
        equation = forTest()
        equationPart1 = equation.first
        equationPart2 = equation.second
        test1 = \
            {
                'coefficient': '1', 'sign': '+',
                'operation':
                    [
                        {
                            'parenthesis':
                                [
                                    {
                                        'sign': '+',
                                        'coefficient': '1',
                                        'variable': 'a'
                                    },
                                    {
                                        'number': 5,
                                        'coefficient': '1',
                                        'sign': '+'
                                    }
                                ],
                            'coefficient': '1',
                            'sign': '+'
                        },
                        {
                            'parenthesis':
                                [
                                    {
                                        'sign': '+',
                                        'coefficient': '1',
                                        'number': 3
                                    },
                                    {
                                        'variable': 'x',
                                        'coefficient': '1',
                                        'sign': '-'
                                    }
                                ],
                            'sign': '*',
                            'coefficient': '1',
                        },
                ],
            }
        test2 = {'number': 5, 'coefficient': '1', 'sign': '+', 'resolution': False}

        self.assertEqual(equationPart1, test1)
        self.assertEqual(equationPart2, test2)

    @patch('computerTest.get_input', return_value='(a + 5) * (3 - x) +(x)= 5')
    def test_first_part_operation4(self, input):
        equation = forTest()
        equationPart1 = equation.first
        equationPart2 = equation.second
        test1 = \
            {
                'coefficient': '1', 'sign': '+',
                'operation':
                    [
                        {
                            'parenthesis':
                                [
                                    {
                                        'sign': '+',
                                        'coefficient': '1',
                                        'variable': 'a'
                                    },
                                    {
                                        'number': 5,
                                        'coefficient': '1',
                                        'sign': '+'
                                    }
                                ],
                            'coefficient': '1',
                            'sign': '+'
                        },
                        {
                            'parenthesis':
                                [
                                    {
                                        'sign': '+',
                                        'coefficient': '1',
                                        'number': 3
                                    },
                                    {
                                        'variable': 'x',
                                        'coefficient': '1',
                                        'sign': '-'
                                    }
                                ],
                            'sign': '*',
                            'coefficient': '1',
                        },
                        {
                            'variable': 'x',
                            'coefficient': '1',
                            'sign': '+'
                        }
                ],
            }
        test2 = {'number': 5, 'coefficient': '1', 'sign': '+', 'resolution': False}
        self.assertEqual(equationPart1, test1)
        self.assertEqual(equationPart2, test2)

    @patch('computerTest.get_input', return_value='(a + 5) * (3 - x) + funcA(x)= 5')
    def test_first_part_operation5(self, input):
        equation = forTest()
        equationPart1 = equation.first
        equationPart2 = equation.second
        test1 = \
            {
                'coefficient': '1', 'sign': '+',
                'operation':
                    [
                        {
                            'parenthesis':
                                [
                                    {
                                        'sign': '+',
                                        'coefficient': '1',
                                        'variable': 'a'
                                    },
                                    {
                                        'number': 5,
                                        'coefficient': '1',
                                        'sign': '+'
                                    }
                                ],
                            'coefficient': '1',
                            'sign': '+'
                        },
                        {
                            'parenthesis':
                                [
                                    {
                                        'sign': '+',
                                        'coefficient': '1',
                                        'number': 3
                                    },
                                    {
                                        'variable': 'x',
                                        'coefficient': '1',
                                        'sign': '-'
                                    }
                                ],
                            'coefficient': '1',
                            'sign': '*'
                        },
                        {
                            'function': {'name': 'funcA', 'variable': 'x', 'coefficient': '1', 'sign': '+'},
                            'coefficient': '1',
                            'sign': '+'
                        }
                    ],
            }
        test2 = {'number': 5, 'coefficient': '1', 'sign': '+', 'resolution': False}

        self.assertEqual(equationPart1, test1)
        self.assertEqual(equationPart2, test2)

    @patch('computerTest.get_input', return_value='(a + 5) * (4 / (3 - x)) = 5')
    def test_first_part_operation6(self, input):
        equation = forTest()
        equationPart1 = equation.first
        equationPart2 = equation.second
        test1 = \
            {
                'coefficient': '1', 'sign': '+',
                'operation':
                 [
                     {'parenthesis': [{'variable': 'a', 'coefficient': '1', 'sign': '+'}, {'number': 5, 'coefficient': '1', 'sign': '+'}],
                      'coefficient': '1',
                      'sign': '+'},

                     {'parenthesis': [
                         {'number': 4, 'coefficient': '1', 'sign': '+'},
                         {'parenthesis': [
                            {'number': 3, 'coefficient': '1', 'sign': '+'},
                            {'variable': 'x', 'coefficient': '1', 'sign': '-'}],
                         'coefficient': '1',
                         'sign': '/'}],
                     'coefficient': '1',
                     'sign': '*'}
                 ],
            }
        test2 = {'number': 5, 'coefficient': '1', 'sign': '+', 'resolution': False}

        self.assertEqual(equationPart1, test1)
        self.assertEqual(equationPart2, test2)

    @patch('computerTest.get_input', return_value='(a + 5) = 5')
    def test_first_part_operation7(self, input):
        equation = forTest()
        equationPart1 = equation.first
        equationPart2 = equation.second
        test1 = \
            {
                'coefficient': '1',
                'sign': '+',
                'operation': [
                    {'sign': '+',
                     'coefficient': '1',
                     'parenthesis': [
                        {'variable': 'a', 'coefficient': '1', 'sign': '+'},
                        {'number': 5, 'coefficient': '1', 'sign': '+'}
                    ]}
                ],
            }
        test2 = {'number': 5, 'coefficient': '1', 'sign': '+', 'resolution': False}

        self.assertEqual(equationPart1, test1)
        self.assertEqual(equationPart2, test2)


    @patch('computerTest.get_input', return_value='funcA(a + 5) * (4 / (3 - x)) = 5')
    def test_first_part_function(self, input):
        equation = forTest()
        equationPart1 = equation.first
        equationPart2 = equation.second
        test1 = {
            'coefficient': '1', 'sign': '+',
            'operation':
                      [
                          {'sign': '+', 'coefficient': '1', 'function': {'name': 'funcA', 'coefficient': '1', 'sign': '+', 'operation': [
                              {'sign': '+', 'coefficient': '1', 'variable': 'a'}, {'sign': '+', 'coefficient': '1', 'number': 5}]}},
                          {'sign': '*', 'coefficient': '1', 'parenthesis': [
                              {'sign': '+', 'coefficient': '1', 'number': 4},
                              {'sign': '/', 'coefficient': '1', 'parenthesis': [
                                  {'sign': '+', 'coefficient': '1', 'number': 3},
                                  {'sign': '-', 'coefficient': '1', 'variable': 'x'}
                              ]}]}
                      ],
        }
        test2 = {'number': 5, 'coefficient': '1', 'sign': '+', 'resolution': False}

        self.assertEqual(equationPart1, test1)
        self.assertEqual(equationPart2, test2)

    @patch('computerTest.get_input', return_value='funcA(5) = ?')
    def test_first_part_function2(self, input):
        equation = forTest()
        equationPart1 = equation.first
        equationPart2 = equation.second
        test1 = {
            'coefficient': '1', 'sign': '+',
            'operation': [{
                'function': {
                    'number': 5,
                    'sign': '+',
                    'coefficient': '1',
                    'name': 'funcA'},
                'coefficient': '1',
                "sign": '+'}
            ],
        }
        test2 = {'resolution': True}

        self.assertEqual(equationPart1, test1)
        self.assertEqual(equationPart2, test2)

    @patch('computerTest.get_input', return_value='funcA(a + 5) * (4 / (3 - x)) + [[2, 3]; [1, 2]; [4, 5]] = 5')
    def test_first_part_function3(self, input):
        equation = forTest()
        equationPart1 = equation.first
        equationPart2 = equation.second
        test1 = {
            'coefficient': '1', 'sign': '+',
            'operation':
                      [
                          {'sign': '+', 'coefficient': '1', 'function': {'name': 'funcA', 'coefficient': '1', 'sign': '+', 'operation': [
                              {'sign': '+', 'coefficient': '1', 'variable': 'a'}, {'sign': '+', 'coefficient': '1', 'number': 5}]}},
                          {'sign': '*', 'coefficient': '1', 'parenthesis': [
                              {'sign': '+', 'coefficient': '1', 'number': 4},
                              {'sign': '/', 'coefficient': '1', 'parenthesis': [
                                  {'sign': '+', 'coefficient': '1', 'number': 3},
                                  {'sign': '-', 'coefficient': '1', 'variable': 'x'}
                              ]}]},
                          {
                              'matrice': [
                                  [{'number': 2, 'coefficient': '1', 'sign': '+'}, {'number': 3, 'coefficient': '1', 'sign': '+'}],
                                  [{'number': 1, 'coefficient': '1', 'sign': '+'}, {'number': 2, 'coefficient': '1', 'sign': '+'}],
                                  [{'number': 4, 'coefficient': '1', 'sign': '+'}, {'number': 5, 'coefficient': '1', 'sign': '+'}]
                              ],
                              'sign': '+',
                              'coefficient': '1'
                          }
                      ],
        }
        test2 = {'number': 5, 'coefficient': '1', 'sign': '+', 'resolution': False}

        self.assertEqual(equationPart1, test1)
        self.assertEqual(equationPart2, test2)

    @patch('computerTest.get_input', return_value='funcA(a + 5)^2 * (4^puissance / (3 - x^5)) + [[2, 3]; [1, 2]; [4, 5]]^5 = 5')
    def test_first_part_puissance(self, input):
        equation = forTest()
        equationPart1 = equation.first
        equationPart2 = equation.second
        test1 = {
            'coefficient': '1', 'sign': '+',
            'operation':
                [
                    {'sign': '+', 'coefficient': '2',
                     'function': {'name': 'funcA', 'coefficient': '1', 'sign': '+', 'operation': [
                         {'sign': '+', 'coefficient': '1', 'variable': 'a'},
                         {'sign': '+', 'coefficient': '1', 'number': 5}]}},
                    {'sign': '*', 'coefficient': '1', 'parenthesis': [
                        {'sign': '+', 'coefficient': 'puissance', 'number': 4},
                        {'sign': '/', 'coefficient': '1', 'parenthesis': [
                            {'sign': '+', 'coefficient': '1', 'number': 3},
                            {'sign': '-', 'coefficient': '5', 'variable': 'x'}
                        ]}]},
                    {
                        'matrice': [
                            [{'number': 2, 'coefficient': '1', 'sign': '+'},
                             {'number': 3, 'coefficient': '1', 'sign': '+'}],
                            [{'number': 1, 'coefficient': '1', 'sign': '+'},
                             {'number': 2, 'coefficient': '1', 'sign': '+'}],
                            [{'number': 4, 'coefficient': '1', 'sign': '+'},
                             {'number': 5, 'coefficient': '1', 'sign': '+'}]
                        ],
                        'sign': '+',
                        'coefficient': '5'
                    }
                ],
        }
        test2 = {'number': 5, 'coefficient': '1', 'sign': '+', 'resolution': False}

        self.assertEqual(equationPart1, test1)
        self.assertEqual(equationPart2, test2)

    @patch('computerTest.get_input', return_value='3x + 2 = 5 ?')
    def test_construction(self, input):
        equation = forTest()
        equationPart1 = equation.first
        equationPart2 = equation.second
        test1 = {'coefficient': '1',
                  'operation': [
                      {'coefficient': '1', 'number': 3, 'sign': '+'},
                      {'coefficient': '1', 'sign': '*', 'variable': 'x'},
                      {'coefficient': '1', 'number': 2, 'sign': '+'}],
                  'sign': '+'}
        test2 = {'number': 5, 'coefficient': '1', 'sign': '+', 'resolution': True}

        self.assertEqual(equationPart1, test1)
        self.assertEqual(equationPart2, test2)

    @patch('computerTest.get_input', return_value='3x + 2i = 5')
    def test_construction_imaginaire(self, input):
        equation = forTest()
        equationPart1 = equation.first
        equationPart2 = equation.second
        test1 = {'coefficient': '1',
                  'operation': [
                      {'coefficient': '1', 'number': 3, 'sign': '+'},
                      {'coefficient': '1', 'sign': '*', 'variable': 'x'},
                      {'coefficient': '1', 'number': 2, 'sign': '+'},
                      {'coefficient': '1', 'imaginaire': 'i', 'sign': '*'}],
                  'sign': '+'}
        test2 = {'number': 5, 'coefficient': '1', 'sign': '+', 'resolution': False}

        self.assertEqual(equationPart1, test1)
        self.assertEqual(equationPart2, test2)

if __name__ == '__main__':
    main()



