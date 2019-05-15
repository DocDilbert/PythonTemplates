from cProfile import Profile
from pstats import Stats
import webscraper
prof = Profile()

prof.disable()  # i.e. don't time imports
import time
prof.enable()  # profiling back on


webscraper.main()
prof.disable()  # don't profile the generation of stats
prof.dump_stats('mystats.stats')

with open('mystats_output.txt', 'wt') as output:
    stats = Stats('mystats.stats', stream=output)
    stats.sort_stats('cumulative', 'time')
    stats.print_stats()