import crawlers
import hotspot
import kgraph

# local crawler test
# crawlers.run(
#     proxies={
#         "http": "http://127.0.0.1:10809",
#         "https": "http://127.0.0.1:10809"
#     }
# )

# # local hotspot generate test
hotspot.run()

# # local knowledge graph test
# kgraph.run()