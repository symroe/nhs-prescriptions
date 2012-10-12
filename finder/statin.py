"""
Locate interesting things related to Statin usage in the
NHS Prescribing data.
"""
import collections
import json
import sys

import argparse
import ffs

blacklist = [ # Things that look interesting but aren't.
    'nystatin'
    ]

data = ffs.Path('../data/prescriptions')
scrips = data.ls('*IEXT.CSV')


def changes(args):
    """
    Herein we look for changes in the proportion of prescribing habit for a subset of
    the UK Prescribing data.

    It is assumed that you have already extracted the subset of drugs you are interested
    in to a CSV file that follows the same format as the main data.

    Done that? then we'll begin by grouping the prescriptions by practice, by period.

    """
    scrips = ffs.Path(args.filename)
    grouped = collections.defaultdict(lambda:collections.defaultdict(lambda:collections.defaultdict(dict)))
    with scrips.csv(header=True) as csv:
        for row in csv:
            if row.items == 'items':
                continue # This is something pointless and stupid. Will find out what later
            grouped[row.practice.strip()][row.period.strip()][row.bnf_name.lower().strip()]['num'] = int(row.items)

    for practice in grouped:
        periods = list(sorted(grouped[practice].keys()))
        for i, period in enumerate(periods):
            scrips = grouped[practice][period]
            total = sum([s['num'] for s in scrips.values()])
            for name, value in scrips.items():
                per = int(float(value['num']) / total * 100)
                grouped[practice][period][name]['per'] = per

                if i > 0:
                    prev = grouped[practice][periods[i-1]][name]
                    try:
                        change = per - prev['per']
                    except KeyError:
                        pass # For now
                    grouped[practice][period][name]['change'] = change


    for practice, history in grouped.items():
        for month, scrips in history.items():
            for drug, stats in scrips.items():
                if 'change' in stats and abs(stats['change']) > 10:
                    print 'YAY', practice, month, drug, stats['change']



        #    print json.dumps(grouped, indent=2)

def extract(args):
    """
    Extract just the Statins please
    """
    frist = scrips[0]
    juststats = data/'{0}.csv'.format(args.searchterm)
    hasheader = False
    stats = 0

    with juststats.csv() as outfile:
        for scrip in scrips:
            with scrip.csv(header=True) as csv:
                if not hasheader:
                    outfile.writerow(csv.rowklass._fields)
                try:
                    for row in csv:
                        name = row.bnf_name.lower().strip()
                        if args.searchterm in name and name not in blacklist:
                            stats += 1
                            sys.stdout.write('.')
                            if stats % 30 == 0:
                                sys.stdout.write('\n')
                            sys.stdout.flush()
                            outfile.writerow(row)
                except Exception as err:
                    import pdb;pdb.set_trace()
                    err # So far this is mostly a failure in the header "magic".
                        # frankly, at this point I don't really care about missing a
                        # couple points from several million.


def main():
    """
    Entrypoint
    """
    parser = argparse.ArgumentParser(description='Scrip Searcher')
    subparsers = parser.add_subparsers(title='Actions')

    parser_extract = subparsers.add_parser('extract')
    parser_extract.add_argument('searchterm', help='Term you want to search for in the name')
    parser_extract.set_defaults(fn=extract)

    parser_changes = subparsers.add_parser('changes', help=changes.__doc__)
    parser_changes.add_argument('filename', help='File you want to look in')
    parser_changes.set_defaults(fn=changes)

    args = parser.parse_args()
    args.fn(args)


if __name__ == '__main__':
    main()
