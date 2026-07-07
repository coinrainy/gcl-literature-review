# Phase 2 First Round Run Log

- Started: 2026-07-07 17:17:32 +08:00
- Scope: Cora, Citeseer, PubMed, Chameleon, Squirrel, Actor
- Required commands per dataset: compute_graph_statistics.py; simulate_positive_view_failure.py with augmentation=edge_drop, rates=0.1 0.2 0.4 0.6 0.8, num-trials=5; diagnose_negative_pair_noise.py with batch-sizes=128 256 512 1024, top-k=5 10 20 50, num-batches=50.
- Labels are used only for post-hoc diagnostic analysis; no training, augmentation decision, or pair weighting uses labels.
- Runner policy: load each dataset once via compute_graph_statistics.py; if PyG download/load fails, record the reason and skip the remaining scripts for that dataset.

## Cora
- ❌ compute_graph_statistics: failed (32.73s), exit=1
- Skipped simulate_positive_view_failure and diagnose_negative_pair_noise because the dataset could not be loaded/downloaded.
```text
    raise return_result
  File "F:\Anaconda\Lib\site-packages\fsspec\asyn.py", line 56, in _runner
    result[0] = await coro
                ^^^^^^^^^^
  File "F:\Anaconda\Lib\site-packages\fsspec\implementations\http.py", line 521, in _isdir
    return bool(await self._ls(path))
                ^^^^^^^^^^^^^^^^^^^^
  File "F:\Anaconda\Lib\site-packages\fsspec\implementations\http.py", line 207, in _ls
    out = await self._ls_real(url, detail=detail, **kwargs)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "F:\Anaconda\Lib\site-packages\fsspec\implementations\http.py", line 159, in _ls_real
    async with session.get(self.encode_url(url), **self.kwargs) as r:
               ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "F:\Anaconda\Lib\site-packages\aiohttp\client.py", line 1423, in __aenter__
    self._resp: _RetType = await self._coro
                           ^^^^^^^^^^^^^^^^
  File "F:\Anaconda\Lib\site-packages\aiohttp\client.py", line 701, in _request
    conn = await self._connector.connect(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        req, traces=traces, timeout=real_timeout
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "F:\Anaconda\Lib\site-packages\aiohttp\connector.py", line 544, in connect
    proto = await self._create_connection(req, traces, timeout)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "F:\Anaconda\Lib\site-packages\aiohttp\connector.py", line 1050, in _create_connection
    _, proto = await self._create_direct_connection(req, traces, timeout)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "F:\Anaconda\Lib\site-packages\aiohttp\connector.py", line 1394, in _create_direct_connection
    raise last_exc
  File "F:\Anaconda\Lib\site-packages\aiohttp\connector.py", line 1363, in _create_direct_connection
    transp, proto = await self._wrap_create_connection(
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<7 lines>...
    )
    ^
  File "F:\Anaconda\Lib\site-packages\aiohttp\connector.py", line 1124, in _wrap_create_connection
    raise client_error(req.connection_key, exc) from exc
aiohttp.client_exceptions.ClientConnectorError: Cannot connect to host github.com:443 ssl:default [Connect call failed ('20.205.243.166', 443)]
```

## Citeseer
- ✅ compute_graph_statistics: success (4.11s)
- ✅ simulate_positive_view_failure: success (23.34s)
- ✅ diagnose_negative_pair_noise: success (5.6s)

## PubMed
- ✅ compute_graph_statistics: success (5.01s)
- ✅ simulate_positive_view_failure: success (71.93s)
- ✅ diagnose_negative_pair_noise: success (5.44s)

## Chameleon
- ✅ compute_graph_statistics: success (3.9s)
- ✅ simulate_positive_view_failure: success (18.64s)
- ✅ diagnose_negative_pair_noise: success (4.91s)

## Squirrel
- ✅ compute_graph_statistics: success (4.7s)
- ✅ simulate_positive_view_failure: success (54.46s)
- ✅ diagnose_negative_pair_noise: success (6.05s)

## Actor
- ✅ compute_graph_statistics: success (4.11s)
- ✅ simulate_positive_view_failure: success (25.08s)
- ✅ diagnose_negative_pair_noise: success (5.42s)

- Finished scripts: 2026-07-07 17:22:07 +08:00
