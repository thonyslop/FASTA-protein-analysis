from modeller import *
from modeller.automodel import *

env = environ()

env.schedule_scale = physical.values(default=1.0, soft_sphere=0.7)

# Leer HETATM (incluye iones como Ca2+)
env.io.hetatm = True

a = automodel(env,
              alnfile  = 'alineamiento.pir',
              knowns   = ('template'),
              sequence = 'PLA2Bjarser',
              assess_methods = (assess.DOPE, assess.GA341))

a.starting_model = 1
a.ending_model   = 100
a.deviation      = 4.0

# Amount of randomization between models
a.generate_method = generate.transfer_xyz
a.rand_method = randomize.xyz

# Very thorough VTFM schedule
a.library_schedule = autosched.slow
a.max_var_iterations = 300

# Thorough MD optimization:
a.md_level = refine.very_slow

a.final_malign3d = True

a.make()

# Get a list of all successfully built models from a.outputs
ok_models = filter(lambda x: x['failure'] is None, a.outputs)

# Rank the models by DOPE score
key = 'DOPE score'
ok_models.sort(lambda a,b: cmp(a[key], b[key]))

# Get top model
m = ok_models[0]
print "Top model: %s (DOPE score %.3f)" % (m['name'], m[key])