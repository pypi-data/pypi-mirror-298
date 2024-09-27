import starsim as ss

# Defining eligibility
def eligibility_function(sim):
    ages = sim.people.age 
    is_eligible = (ages >= 9) & (ages <= 12)
    print(f'Checking eligibility: of {len(ages)} people, {is_eligible.sum()} are eligible')
    return sim.people.auids[is_eligible]

# Define a custom "SIS" vaccine
class sis_vaccine(ss.Vx):
    def __init__(self, pars=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_pars(
            efficacy = 0.9,
        )
        self.update_pars(pars, **kwargs)
        return

    def administer(self, people, uids):
        ages = people.age[uids]
        min_age = ages.min()
        max_age = ages.max()
        rel_sus = people.sis.rel_sus
        rel_sus[uids] *= 1-self.pars.efficacy
        print(f'Administering {len(uids)} doses for people aged {min_age:n} - {max_age:n}; rel_sus={rel_sus.mean():n}')
        return

# Create the product
mcv1 = sis_vaccine()

# Create the intervention
my_intervention1 = ss.routine_vx(
    start_year=2020,
    prob=0.9,         
    product=mcv1,     
    eligibility = eligibility_function # Move this outside of the parameters -- sorry!!
)

# Run the simulation
sim = ss.Sim(diseases='sis', networks='random', interventions=my_intervention1)
sim.run()
sim.plot()
