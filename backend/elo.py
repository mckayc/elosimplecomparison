def rate_1vs1(ra, rb, result):
    K = 32
    ea = 1 / (1 + 10 ** ((rb - ra) / 400))
    eb = 1 / (1 + 10 ** ((ra - rb) / 400))

    if result:
        ra_new = ra + K * (1 - ea)
        rb_new = rb + K * (0 - eb)
    else:
        ra_new = ra + K * (0 - ea)
        rb_new = rb + K * (1 - eb)

    return ra_new, rb_new
