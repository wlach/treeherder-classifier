#!/usr/bin/env python

import MySQLdb
import os
import sys


(host, db_name, user, passwd, ssl_ca, outdir, startdate, enddate) = sys.argv[1:]


db = MySQLdb.connect(
    host=host,
    db=db_name,
    user=user,
    passwd=passwd,
    ssl={'ca': ssl_ca})
c = db.cursor()
c.execute('''
select bjm.id, bjm.bug_id, tle.line from bug_job_map as bjm
  left join text_log_step as tls on tls.job_id = bjm.job_id
  left join text_log_error as tle on tle.step_id = tls.id
  where bjm.created > '%s' and bjm.created < '%s' and bjm.user_id is not NULL and bjm.bug_id is not NULL
  order by bjm.id, tle.step_id, tle.id;
''' % (startdate, enddate))

output = {}
for (bjm_id, bug_id, tle_line) in c.fetchall():
    if not output.get(bjm_id):
        output[bjm_id] = {
            'bug_id': bug_id,
            'lines': []
        }
    if tle_line:
        output[bjm_id]['lines'].append(tle_line)

try:
    os.mkdir(outdir)
except:
    pass

for (bjm_id, bug_entry) in output.iteritems():
    bugdir = os.path.join(outdir, str(bug_entry['bug_id']))
    try:
        os.mkdir(bugdir)
    except:
        pass
    if bug_entry['lines']:
        open(os.path.join(bugdir, '%s.txt' % bjm_id), 'w').write('\n'.join(bug_entry['lines']))

