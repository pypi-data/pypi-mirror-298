from alively import App


def test_app_get_handler(app: App, get_event):
    event = get_event('StatsLine')
    handler = app.get_handler(event)
    assert handler.__name__ == app.handle_StatsLine.__name__


def test_app_handle_StatsLine_event(app: App, get_event):
    event = get_event('StatsLine')
    state = app.handle(event)
    assert event in state.events


def test_app_handles_event_with_no_handler(app: App, get_event):
    event = get_event('StatsLine')
    event.info.name = 'NoHandlerForThis'
    state = app.handle(event)
    assert event in state.events


def test_app_runs(app: App, mock_events):
    assert len(app.state.events) == 0
    res = list(app.run(args=[]))
    assert len(res) == len(mock_events)
    assert app.state.finished
    assert app.state.run_started_at is not None
    assert app.state.invocation_id is not None
    assert app.state.dbt_log_version is not None
    assert app.state.dbt_version is not None
    assert app.state.node_count is not None
    assert app.state.num_threads is not None
    assert app.state.target_name is not None
    assert app.state.adapter_name is not None
    assert app.state.adapter_version is not None
    assert len(app.state.nodes) > 0
    assert len(app.state.nodes_with_status('skipped')) > 0
    assert len(app.state.nodes_with_status('success')) > 0
    assert len(app.state.nodes_with_status('fail')) > 0
    assert len(app.state.nodes_with_status('started')) == 0


def test_app_with_partial_run(app: App):
    # Process only the first 10 events, so that we can check an "in progress" node
    # exists.
    for n, event in enumerate(app.run([])):
        if n == 10:
            break
    assert len(app.state.nodes_with_status('started')) > 0
