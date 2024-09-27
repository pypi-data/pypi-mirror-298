from pytest import mark
from alively.runners import dbtSubprocessRunner


dbt_commands = [
    (['dbt', 'build'], 1),
    (['dbt', 'test'], 1),
    # TODO: handle these other cases
    # (['dbt'], 0)  # this currently passes even though the program hangs
    # (['dbt', '--help'], 0)  # this currently passes even though the program errors with a JSONDeoceder error
    # (['dbt', 'commanddne'], 0)
    # ([], 0)
    # (['dbt', 'build', '--help'], 0)
    # (['dbt', 'commanddne', '--help'], 0)
]

dbt_command_ids = ['-'.join(c) for (c,_) in dbt_commands]

@mark.integration
@mark.parametrize("command,return_code", dbt_commands, ids=dbt_command_ids)
def test_dbt_subprocess_runner(command, return_code, mock_dbt_project):
    runner = dbtSubprocessRunner()
    events = list(runner.run(command))
    assert runner.completed
