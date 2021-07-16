# Additional ULS Features
This document handles the usage of features not explained anywhere else.

## FILTER (--filter) Feature
This feature got introduced in ULS v0.0.5.
It allows to decrease the number of log lines sent to SIEM for cost, performance or security reasons.

The filter is **regex** based so it is capable of filtering "json" AND raw text events. 
Only events **matching the filter pattern will be sent towards the selected SIEM** output.

For ETP there is also an option to [filter directly on the API side](AKAMAI_API_CREDENTIALS.md#etp-api-event-filters).

### Usage examples:
- Filter for "geo_country": "Germany" (in EAA Access logs)
    ```bash
    python3 bin/uls.py -i eaa -f access -o raw <additional params> --filter '.*"geo_country": "Germany".*'
    ```
- Filter for "actionName": "Block - Error Page" (in ETP Threat logs)
    ```bash
    python3 bin/uls.py -i etp -f threat -o raw <additional params> --filter '.*"actionName": "Block - Error Page".*'
    ```
Always test your filter with the "RAW" console output on the command libefore you send the data towards a SIEM
```bash
python3 bin/uls.py -i eaa --feed access --filter '.*"geo_country": "Germany".*' -o raw
```

## RAWCMD (--rawcmd) Feature
This feature got introduced in ULS v0.0.3.
Attention: This is a pretty critical setting, which can break ULS behaviour.

Raw commands within ULS can be used to trigger cli calls, that have not been integrated into ULS (yet).
This allows a more flexible implementation to solve some edge cases.
RAWCMD just requires the input to be selected.

Example: 
```bash
python3 bin/uls.py -i etp --rawcmd 'event threat -f' -l debug -o raw
```
This will also run the etp threat feed in "tail -f" mode

Please be aware: Not all output from the cli will be redirected to ULS by default.