from itertools import repeat
from multiprocessing import Pool

import pytest

from cobra.asset.asset import get_asset
from cobra.robot.robot import get_module_db
from cobra.solution.solution import find_solutions, get_solution
from cobra.task.task import get_task
from cobra.utils import caches
from cobra.utils.schema import get_schema


def _get_task(id):
    return get_task(id=id)


def _get_solution(uuid):
    return get_solution(uuid)[0]


solution_uuids, _ = find_solutions(task_id='simple/PTP_1')


"""
Collection of tests regarding cobra usage in multiprocessing environments.

Such as:
 - File creation race conditions
"""


@pytest.mark.parametrize(
    "test_func, arg",
    [
        (_get_task, "simple/PTP_2"),
        (get_module_db, "modrob-gen2"),
        (get_schema, 'TaskSchema'),
        (get_asset, 'assets/DMU_125P.stl'),
        (_get_solution, solution_uuids[0]),
    ]
)
def test_multiprocessing(test_func, arg, n_iter=10, n_retry=3):
    """Test that get_task works in a multiprocessing environment."""
    with Pool(6) as p:
        for i in range(n_retry):  # Race condition not always reproducible
            caches.reset_cache()
            tasks = p.map(test_func, repeat(arg, n_iter))
            assert len(tasks) == n_iter
            for t in tasks:
                assert t.is_file()
