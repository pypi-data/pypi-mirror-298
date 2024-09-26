import numpy as np
import pandas as pd
import sciris as sc
import pylab as pl
import starsim as ss
np; pd; sc; pl; ss


sim = ss.Sim(
    unit='day', 
    dt=1.0, 
    diseases=dict(
        type='sis', 
        unit='day', 
        dt=0.1,
    ), 
    networks=dict(
        type='random', 
        unit='day', 
        dt=5,
    ),
    dur = 20,
)

sim.run()
sim.plot()
sim.loop.plot()
df = sim.loop.to_df()
print(df)