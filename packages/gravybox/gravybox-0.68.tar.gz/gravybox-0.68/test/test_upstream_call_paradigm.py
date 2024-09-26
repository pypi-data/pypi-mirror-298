from asyncio import sleep

import pytest

from gravybox.betterstack import collect_logger
from gravybox.exceptions import DataUnavailable
from gravybox.protocol import LinkRequest
from gravybox.upstream_call_paradigm import UpstreamCentrifuge, UpstreamSequencer
from test.testkit import sleeping_coroutine, TestTaskResult, none_result_coroutine, failing_coroutine

logger = collect_logger()


@pytest.mark.asyncio
async def test_upstream_centrifuge_single_task():
    link_request = LinkRequest(trace_id="centrifuge")
    tasks = [
        sleeping_coroutine(1, "test", 23, field_three=True, link_request=link_request)
    ]
    centrifuge = UpstreamCentrifuge(tasks, TestTaskResult)
    result = await centrifuge.activate()
    assert result == TestTaskResult(field_one="test", field_two=23, field_three=True)


@pytest.mark.asyncio
async def test_upstream_centrifuge_two_task():
    link_request = LinkRequest(trace_id="double_centrifuge")
    tasks = [
        sleeping_coroutine(1, "test", 23, field_three=True, link_request=link_request),
        sleeping_coroutine(999, "sleepy", 333, field_three=False, link_request=link_request)
    ]
    centrifuge = UpstreamCentrifuge(tasks, TestTaskResult)
    result = await centrifuge.activate()
    assert result == TestTaskResult(field_one="test", field_two=23, field_three=True)


@pytest.mark.asyncio
async def test_upstream_centrifuge_failing_task():
    link_request = LinkRequest(trace_id="failing_centrifuge")
    tasks = [
        sleeping_coroutine(5, "test", 23, field_three=True, link_request=link_request),
        failing_coroutine(1, "failure", 333, field_three=False, link_request=link_request)
    ]
    centrifuge = UpstreamCentrifuge(tasks, TestTaskResult)
    result = await centrifuge.activate()
    assert result == TestTaskResult(field_one="test", field_two=23, field_three=True)


@pytest.mark.asyncio
async def test_upstream_centrifuge_none_result_task():
    link_request = LinkRequest(trace_id="none_centrifuge")
    tasks = [
        sleeping_coroutine(5, "test", 23, field_three=True, link_request=link_request),
        none_result_coroutine(2, None, None, field_three=False, link_request=link_request)
    ]
    centrifuge = UpstreamCentrifuge(tasks, TestTaskResult)
    result = await centrifuge.activate()
    assert result == TestTaskResult(field_one="test", field_two=23, field_three=True)


@pytest.mark.asyncio
async def test_upstream_centrifuge_total_failure():
    link_request = LinkRequest(trace_id="total_failure")
    tasks = [
        failing_coroutine(2, "failure", 333, field_three=False, link_request=link_request),
        failing_coroutine(1, "failure", 333, field_three=False, link_request=link_request)
    ]
    centrifuge = UpstreamCentrifuge(tasks, TestTaskResult)
    with pytest.raises(DataUnavailable):
        await centrifuge.activate()


@pytest.mark.asyncio
async def test_upstream_centrifuge_merge_two_results():
    link_request = LinkRequest(trace_id="centrifuge_merge")
    tasks = [
        sleeping_coroutine(1, None, 23, field_three=True, link_request=link_request),
        sleeping_coroutine(3, "test", None, field_three=True, link_request=link_request),
    ]
    centrifuge = UpstreamCentrifuge(tasks, TestTaskResult)
    result = await centrifuge.activate()
    assert result == TestTaskResult(field_one="test", field_two=23, field_three=True)


@pytest.mark.asyncio
async def test_upstream_centrifuge_merge_overwrite():
    link_request = LinkRequest(trace_id="centrifuge_merge_overwrite")
    tasks = [
        sleeping_coroutine(1, None, None, field_three=True, link_request=link_request),
        sleeping_coroutine(3, "test", None, field_three=True, link_request=link_request),
        sleeping_coroutine(5, "late_precedence", 15, field_three=False, link_request=link_request),
    ]
    centrifuge = UpstreamCentrifuge(tasks, TestTaskResult)
    result = await centrifuge.activate()
    assert result == TestTaskResult(field_one="late_precedence", field_two=15, field_three=False)


@pytest.mark.asyncio
async def test_upstream_centrifuge_merge_empty_strings():
    link_request = LinkRequest(trace_id="centrifuge_merge_empty_strings")
    tasks = [
        sleeping_coroutine(1, "", 23, field_three=True, link_request=link_request),
        sleeping_coroutine(3, "test", None, field_three=True, link_request=link_request),
    ]
    centrifuge = UpstreamCentrifuge(tasks, TestTaskResult)
    result = await centrifuge.activate()
    assert result == TestTaskResult(field_one="test", field_two=23, field_three=True)


@pytest.mark.asyncio
async def test_upstream_centrifuge_chaos():
    link_request = LinkRequest(trace_id="centrifuge_chaos")
    tasks = [
        sleeping_coroutine(99, None, None, field_three=True, link_request=link_request),
        failing_coroutine(33, "failure", 333, field_three=False, link_request=link_request),
        sleeping_coroutine(1, None, None, field_three=True, link_request=link_request),
        none_result_coroutine(3, None, None, field_three=False, link_request=link_request),
        failing_coroutine(1, "failure", 333, field_three=False, link_request=link_request),
        sleeping_coroutine(3, "test", None, field_three=True, link_request=link_request),
        none_result_coroutine(2, None, None, field_three=False, link_request=link_request),
        failing_coroutine(2, "failure", 333, field_three=False, link_request=link_request),
        sleeping_coroutine(5, "late_precedence", 15, field_three=False, link_request=link_request),
        sleeping_coroutine(19, "something_else", 25, field_three=False, link_request=link_request)
    ]
    centrifuge = UpstreamCentrifuge(tasks, TestTaskResult)
    result = await centrifuge.activate()
    assert result == TestTaskResult(field_one="late_precedence", field_two=15, field_three=False)


@pytest.mark.asyncio
async def test_upstream_sequencer_single_task():
    link_request = LinkRequest(trace_id="sequencer")
    tasks = [
        sleeping_coroutine(1, "test", 23, field_three=True, link_request=link_request)
    ]
    sequencer = UpstreamSequencer(tasks, TestTaskResult)
    result = await sequencer.activate()
    assert result == TestTaskResult(field_one="test", field_two=23, field_three=True)


@pytest.mark.asyncio
async def test_upstream_sequencer_two_task():
    link_request = LinkRequest(trace_id="double_sequencer")
    tasks = [
        sleeping_coroutine(1, "test", 23, field_three=True, link_request=link_request),
        sleeping_coroutine(999, "sleepy", 333, field_three=False, link_request=link_request)
    ]
    sequencer = UpstreamSequencer(tasks, TestTaskResult)
    result = await sequencer.activate()
    assert result == TestTaskResult(field_one="test", field_two=23, field_three=True)


@pytest.mark.asyncio
async def test_upstream_sequencer_sequencing():
    link_request = LinkRequest(trace_id="sequencer_sequencing")
    logger.info("adding first upstream call to tasks")
    tasks = [
        sleeping_coroutine(1, None, 23, field_three=True, link_request=link_request)
    ]
    await sleep(1)
    logger.info("adding second upstream call to tasks")
    tasks.append(
        sleeping_coroutine(2, "test", 23, field_three=True, link_request=link_request)
    )
    await sleep(1)
    logger.info("creating sequencer")
    sequencer = UpstreamSequencer(tasks, TestTaskResult)
    await sleep(1)
    logger.info("calling upstreams")
    result = await sequencer.activate()
    assert result == TestTaskResult(field_one="test", field_two=23, field_three=True)


@pytest.mark.asyncio
async def test_upstream_sequencer_failing_task():
    link_request = LinkRequest(trace_id="failing_sequencer")
    tasks = [
        failing_coroutine(1, "failure", 333, field_three=False, link_request=link_request),
        sleeping_coroutine(5, "test", 23, field_three=True, link_request=link_request)
    ]
    sequencer = UpstreamSequencer(tasks, TestTaskResult)
    result = await sequencer.activate()
    assert result == TestTaskResult(field_one="test", field_two=23, field_three=True)


@pytest.mark.asyncio
async def test_upstream_sequencer_none_result_task():
    link_request = LinkRequest(trace_id="none_sequencer")
    tasks = [
        none_result_coroutine(2, None, None, field_three=False, link_request=link_request),
        sleeping_coroutine(5, "test", 23, field_three=True, link_request=link_request)
    ]
    sequencer = UpstreamSequencer(tasks, TestTaskResult)
    result = await sequencer.activate()
    assert result == TestTaskResult(field_one="test", field_two=23, field_three=True)


@pytest.mark.asyncio
async def test_upstream_sequencer_total_failure():
    link_request = LinkRequest(trace_id="total_failure")
    tasks = [
        failing_coroutine(2, "failure", 333, field_three=False, link_request=link_request),
        failing_coroutine(1, "failure", 333, field_three=False, link_request=link_request)
    ]
    sequencer = UpstreamSequencer(tasks, TestTaskResult)
    with pytest.raises(DataUnavailable):
        await sequencer.activate()


@pytest.mark.asyncio
async def test_upstream_sequencer_merge_two_results():
    link_request = LinkRequest(trace_id="sequencer_merge")
    tasks = [
        sleeping_coroutine(1, None, 23, field_three=True, link_request=link_request),
        sleeping_coroutine(3, "test", None, field_three=True, link_request=link_request),
    ]
    sequencer = UpstreamSequencer(tasks, TestTaskResult)
    result = await sequencer.activate()
    assert result == TestTaskResult(field_one="test", field_two=23, field_three=True)


@pytest.mark.asyncio
async def test_upstream_sequencer_merge_overwrite():
    link_request = LinkRequest(trace_id="sequencer_merge_overwrite")
    tasks = [
        sleeping_coroutine(1, None, None, field_three=True, link_request=link_request),
        sleeping_coroutine(3, "test", None, field_three=True, link_request=link_request),
        sleeping_coroutine(5, "late_precedence", 15, field_three=False, link_request=link_request),
    ]
    sequencer = UpstreamSequencer(tasks, TestTaskResult)
    result = await sequencer.activate()
    assert result == TestTaskResult(field_one="late_precedence", field_two=15, field_three=False)


@pytest.mark.asyncio
async def test_upstream_centrifuge_merge_empty_strings():
    link_request = LinkRequest(trace_id="sequencer_merge_empty_strings")
    tasks = [
        sleeping_coroutine(1, "", 23, field_three=True, link_request=link_request),
        sleeping_coroutine(3, "test", None, field_three=True, link_request=link_request),
    ]
    sequencer = UpstreamSequencer(tasks, TestTaskResult)
    result = await sequencer.activate()
    assert result == TestTaskResult(field_one="test", field_two=23, field_three=True)


@pytest.mark.asyncio
async def test_upstream_sequencer_chaos():
    link_request = LinkRequest(trace_id="sequencer_chaos")
    tasks = [
        sleeping_coroutine(1, None, None, field_three=True, link_request=link_request),
        failing_coroutine(1, "failure", 333, field_three=False, link_request=link_request),
        none_result_coroutine(3, None, None, field_three=False, link_request=link_request),
        none_result_coroutine(2, None, None, field_three=False, link_request=link_request),
        failing_coroutine(2, "failure", 333, field_three=False, link_request=link_request),
        sleeping_coroutine(5, "late_precedence", 15, field_three=False, link_request=link_request),
        sleeping_coroutine(3, "test", None, field_three=True, link_request=link_request),
        sleeping_coroutine(99, None, None, field_three=True, link_request=link_request),
        failing_coroutine(33, "failure", 333, field_three=False, link_request=link_request),
        sleeping_coroutine(19, "something_else", 25, field_three=False, link_request=link_request)
    ]
    sequencer = UpstreamSequencer(tasks, TestTaskResult)
    result = await sequencer.activate()
    assert result == TestTaskResult(field_one="late_precedence", field_two=15, field_three=False)
