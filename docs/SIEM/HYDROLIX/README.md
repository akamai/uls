# Hydrolix integration

ULS is able to send any [supported feeds](../LOG_OVERVIEW.md) to Hydrolix with HTTP Output.  
Make sure you turn off the HTTP Liveness check since Hydrolix Ingestion endpoints do not accept HTTP HEAD requests.

## Example ULS pushing to Hydrolix

Docker example with Guardicore netlog feed:

```bash
docker run -d --name uls_gc_netlog -ti \
    --mount type=bind,source="/path/to/your/.edgerc",target="/opt/akamai-uls/.edgerc",readonly \
    --env ULS_INPUT=GC \
    --env ULS_FEED=NETLOG \
    --env ULS_OUTPUT=HTTP \
    --env GC_SKIP_TLS_VALIDATION=True \
    --env ULS_HTTP_URL='https://iad.trafficpeak.live/ingest/event?table=xxxxx' \
    --env ULS_HTTP_AUTH_HEADER='{"Authorization": "Basic xxxx=="}' \
    --env ULS_HTTP_LIVNESS_CHECK=false \
    --env ULS_HTTP_FORMAT="%s" \
    akamai/uls
```

## More information

See Hydrolix website [https://www.hydrolix.com ](https://hydrolix.io/)