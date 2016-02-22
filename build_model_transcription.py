#import antimony
import csv

out = ''

comps = set()

id_map = {}

# Species
with open('Transcription_SP.csv', 'rU') as f:
  r = csv.reader(f, delimiter=',', dialect=csv.excel_tab)
  for row in list(r)[1:]:
    #print(row)
    # ID
    id_ = row[0]
    # Display name
    name = row[1]
    # Compartment
    comp = row[2]
    # Copy number
    copies = int(row[3])
    # Type
    tp = row[4]
    # Role
    role = row[5]

    new_id = id_ + '__' + comp

    id_map[id_] = id_ + '__' + comp

    out += '  var species {};\n'.format(new_id)
    # initial conc.
    out += '  {} = {}/{};\n'.format(new_id, copies, comp)
    #out += '  {} = {} items;\n'.format(new_id, copies, comp)
    # compartment
    out += '  {} in {};\n'.format(new_id, comp)
    # display name
    out += '  {} is "{}";\n'.format(new_id, name)

    comps.add(comp)

    out += '\n'

for c in comps:
  out = '  const compartment {};\n\n'.format(c) + out

out = '  Km1_tx = 1;\n  Km2_tx = 1;\n  Km3_tx = 1;\n  Km4_tx = 1;\n' + out
out = '  unit substance = item\n\n' + out
out = 'model transcription()\n' + out
out = 'function min(x,y)\n  piecewise(x,x<y,y)\nend\n\n' + out

import re

# Reactions
with open('Transcription_RX.csv', 'rU') as f:
  r = csv.reader(f, delimiter=',', dialect=csv.excel_tab)
  for row in list(r)[1:]:
    #id_ = row[0][14:]
    id_ = row[0]
    name = row[1]
    stoich = row[2]
    ratelaw = row[4]
    rateparams = row[5]

    # perform species name conversion on stoichiometry
    new_stoich = stoich
    for k,v in id_map.iteritems():
      new_stoich = re.sub(r'\b{}\b'.format(k),v,new_stoich)

    # perform species name conversion on ratelaw
    new_ratelaw = ratelaw
    for k,v in id_map.iteritems():
      new_ratelaw = re.sub(r'\b{}\b'.format(k),v,new_ratelaw)

    out += '  {}: {}; {};\n'.format(id_, new_stoich, new_ratelaw)
    out += '  {};\n'.format(rateparams)
    # display name
    out += '  {} is "{}";\n'.format(id_, name)

    out += '\n'

out += 'end'

#print(out)
#print(comps)

with open('transcription.sb', 'w') as f:
  f.write(out)