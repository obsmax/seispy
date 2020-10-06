#!/usr/bin/env python
import sys, glob, os
from seispy import readseispystream, Stream, Trace

# ===== defaults
options = {"-v": False,
           "-m": 1,
           "-g": 0.1,
           "-pg": 0.8,
           "prepro": []}

# =====
HELP = """viz
-h            help message
-v            verbose
# ====== display options
-m  i         mode 1=show 2=shade 12=both
-g  f         gain (for mode 0)
-pg  f        powergain (for mode 1)
# ====== preprocessing options (ordered)
-d            detrend
-bp f f f     bandpass fmin, fmax, order
-gbp f f      Gaussian bandpass fcenter, alpha
"""


def read_arguments():
    global options
    argv = sys.argv[1:]

    if len(argv) == 0 or "-h" in argv:
        print(HELP)
        exit(0)

    while len(argv):
        arg = argv.pop(0)
        if arg.startswith('--'):
            # some options
            raise NotImplementedError(arg)

        elif arg.startswith('-'):
            # ============= 1 x bool
            if arg in ["-v"]:
                options[arg] = True

            # ============= 1 x int
            elif arg in ["-m"]:
                options[arg] = int(argv.pop(0))

            # ============= 1 x float
            elif arg in ["-g", "-pg"]:
                options[arg] = float(argv.pop(0))

            # ============= prepro
            elif arg == "-d":
                options['prepro'].append(('-d', ))

            elif arg == "-bp":
                fmin = float(argv.pop(0))
                fmax = float(argv.pop(0))
                order = float(argv.pop(0))
                options['prepro'].append(('-bp', fmin, fmax, order))

            elif arg == "-gbp":
                fcenter = float(argv.pop(0))
                alpha = float(argv.pop(0))
                options['prepro'].append(('-gbp', fcenter, alpha))

            else:
                raise NotImplementedError(arg)

        elif arg.endswith('.seispystream.npz'):
            npzfile = arg

    return npzfile, options


def prepro(st: Stream, options):
    for arg in options['prepro']:
        cmd = arg[0]
        if cmd == "-d":
            for tr in st:
                tr.detrend()

        elif cmd == "-bp":
            fmin, fmax, order = arg[1:]
            for tr in st:
                tr.bandpass(
                    freqmin=fmin, freqmax=fmax,
                    order=order, zerophase=True)

        elif cmd == "-gbp":
            fcenter, alpha = arg[1:]
            for tr in st:
                tr.gaussbandpass(freq0=fcenter, alpha=alpha)

    if options['-v']:
        for tr in st:
            print(tr)


if __name__ == '__main__':
    npzfile, options = read_arguments()

    st = readseispystream(npzfile)
    st.sort_by('distance')

    prepro(st, options)

    if options['-m'] == 1:
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111)
        st.show(ax, gain=options['-g'], seedticks=True)

        plt.show()
    elif options['-m'] == 2:
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111)
        st.shade(ax, powergain=options['-pg'])
        plt.show()

    elif options['-m'] == 12:
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111)
        st.shade(ax, powergain=options['-pg'], cmap=plt.get_cmap("seismic"))
        st.show(ax, gain=options['-g'])
        plt.show()

    else:
        raise NotImplementedError