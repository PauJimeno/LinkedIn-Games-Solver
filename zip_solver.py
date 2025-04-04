from pprint import pprint

from src.solver.ZipSolver import ZipSolver

INSTANCE_15 = {
    'walls': {
        0: ['DOWN'],
        3: ['DOWN'],
        5: ['DOWN'],
        6: ['DOWN'],
        8: ['DOWN'],
        10: ['RIGHT'],
        12: ['DOWN'],
        15: ['RIGHT'],
        17: ['DOWN', 'RIGHT'],
        19: ['RIGHT'],
        22: ['RIGHT'],
        23: ['RIGHT'],
        26: ['DOWN', 'RIGHT'],
        29: ['RIGHT'],
        30: ['RIGHT'],
        31: ['DOWN'],
        33: ['RIGHT'],
        36: ['DOWN', 'RIGHT'],
        37: ['DOWN'],
        40: ['DOWN', 'RIGHT']
    },
    'ordered_sequence': [0, 3, 6],
    'size': 7
}


zip_solver = ZipSolver(INSTANCE_15['walls'], INSTANCE_15['ordered_sequence'], INSTANCE_15['size'])

if zip_solver.solve_puzzle():
    print(f'Zip solved in {zip_solver.computing_time}')
    pprint(zip_solver.get_model())

