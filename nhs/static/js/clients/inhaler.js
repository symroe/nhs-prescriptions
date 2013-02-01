
var inhalerCodes = {
    "naughty": [
        "0301011R0BMAAAP",
        "0301011R0BJABAF",
        "0301011E0BDAAAD",
        "0302000N0AAAXAX",
        "0302000N0AABFBF",
        "0302000N0AABGBG",
        "0302000N0AAAYAY",
        "0302000N0AABEBE",
        "0302000N0AAAZAZ",
        "0302000N0BDABBK",
        "0302000N0BDACBL",
        "0302000C0BQAABX",
        "0301011R0BIAGBU",
        "0301011R0BIAAAA",
        "0301011R0BIAHAP",
        "0301011R0BIAFAP",
        "0301011R0BXABCC",
        "0301011R0BXAACB",
        "0301011U0AAACAC",
        "0301011U0AAAHAH",
        "0301011U0AAAEAE",
        "0301011U0AAABAB",
        "0301011U0AAAAAA"
    ],
    "nice": [
        "0302000K0AAALAL",
        "0302000K0AAAMAM",
        "0302000K0AAAUAU",
        "0301011E0BBAAAA",
        "0301011E0AAADAD",
        "0301011E0AAACAC",
        "0301011E0AAABAB",
        "0301011E0AAAAAA",
        "0301011X0BBAAAA",
        "0301011X0BBABAB",
        "0301011R0BTAABX",
        "0301040R0AAAAAA",
        "0301011R0AAAXAX",
        "0301011R0AABDBD",
        "0301011R0AABBBB",
        "0301011R0AAAPAP",
        "0301011R0AAADAD",
        "0301011R0AABUBU",
        "0301011R0AABZBZ",
        "0301011R0AACCCC",
        "0301011R0AACBCB",
        "0301011R0AABYBY",
        "0301011R0AACACA",
        "0301011R0AAAQAQ",
        "0301011R0AAAFAF",
        "0301011R0AAAVAV",
        "0301011R0AAAWAW",
        "0301011U0BBACAC"
    ]

$(document).ready(function(){

    Scrip.practice.bucket_compare(
        naughty: inhalerCodes.naughty,
        nice: inhalerCodes.nice,
        map: map
    );

    Scrip.ccg.bucket_compare({
        naughty: inhalerCodes.naughty,
        nice: inhalerCodes.nice,
        map: map

    });
})

//{"A81016": {"group1": {"items": 1, "proportion": 100}, "group2": {"items": 0, "proportion": 0}}}
