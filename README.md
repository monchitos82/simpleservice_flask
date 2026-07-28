# flask-simple-service
simple-service used to test some observability features in metrics exporter and otel

This is a simple Flask service that I used to mess with the Prometheus and OTEL instrumentation. At one point in time I tried Honeycomb and Graylog, but there was no win, so I stick to metrics and traces.

Most of the boilerplate on this project was generated using Chat-GPT and fixed by me. I know what I'm doing here, but things like unit tests or the modeling are simple enough to let an LLM take care.

The credentials are dummy values, so I don't care if a scrapper collects them, they have no use but to be placeholders.

This is the prompt used to generate most of the code:
"This service works with OTEL and Prometheus, you will need a scrapper and a database in postgres but so far everything is working."

The downstream call was added into the `/data` call, nothing fancy, the remote service should return a string, for testing I just created another service with a call to random: ```''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))``` If you there's no downstream, it can use the `/random` endpoint in this project.
