## 1.27.5 - 2024-09-28
### Extractors
#### Additions
- [ao3] add support ([#6013](https://github.com/mikf/gallery-dl/issues/6013))
- [civitai] add support ([#3706](https://github.com/mikf/gallery-dl/issues/3706), [#3787](https://github.com/mikf/gallery-dl/issues/3787), [#4129](https://github.com/mikf/gallery-dl/issues/4129), [#5995](https://github.com/mikf/gallery-dl/issues/5995), [#6220](https://github.com/mikf/gallery-dl/issues/6220))
- [cohost] add support ([#4483](https://github.com/mikf/gallery-dl/issues/4483), [#6191](https://github.com/mikf/gallery-dl/issues/6191))
#### Fixes
- [8chan] update `TOS` cookie name
- [deviantart] work around OAuth API returning empty journal texts ([#6196](https://github.com/mikf/gallery-dl/issues/6196), [#6207](https://github.com/mikf/gallery-dl/issues/6207), [#5916](https://github.com/mikf/gallery-dl/issues/5916))
- [weasyl:favorite] fix pagination ([#6113](https://github.com/mikf/gallery-dl/issues/6113))
#### Improvements
- [bluesky] support video downloads ([#6183](https://github.com/mikf/gallery-dl/issues/6183))
- [deviantart] add `previews` option ([#3782](https://github.com/mikf/gallery-dl/issues/3782), [#6124](https://github.com/mikf/gallery-dl/issues/6124))
- [deviantart] warn about empty journal texts ([#5916](https://github.com/mikf/gallery-dl/issues/5916))
- [inkbunny:favorite] update default directory ([#6115](https://github.com/mikf/gallery-dl/issues/6115))
- [jpgfish] update domain to `jpg5.su` ([#6231](https://github.com/mikf/gallery-dl/issues/6231))
- [skeb] prevent 429 errors and need for `request_key` cookie
- [weasyl:favorite] support readable URL format ([#6113](https://github.com/mikf/gallery-dl/issues/6113))
- [wikimedia] automatically detect API endpoint when none is defined
- [zzup] support `up.zzup.com` galleries ([#6181](https://github.com/mikf/gallery-dl/issues/6181))
### Post Processors
- [ugoira] implement storing "original" frames in ZIP archives ([#6147](https://github.com/mikf/gallery-dl/issues/6147))
- [ugoira] fix `KeyError: '_ugoira_frame_index'` ([#6154](https://github.com/mikf/gallery-dl/issues/6154))
### Formatter
- add `L` conversion - returns the length of a value
- allow accessing `util.NONE` via global `_nul`
### Miscellaneous
- [cookies] add `cookies-select` option
- [cookies:firefox] support using domain & container filters together
- [docker] prevent errors in Dockerfile build
- [tests] make `#category` result entries optional
- allow filtering `--list-extractors` results
- implement alternatives for deprecated `utc` datetime functions
