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
-m  i         mode 
              trace modes :    0=basic
              stream modes :   
                1  = show
                11 = show with obspy like decimation 
                2  = shade 
                12 = modes 1 and 2
-g  f         gain (for mode 0)
-pg  f        powergain (for mode 1)
# ====== preprocessing options (ordered)
-d            detrend
-tap f        taper width (s)
-bp f f f     bandpass fmin(Hz), fmax(Hz), order(e.g. 4.)
-gbp f f      Gaussian bandpass fcenter(Hz), alpha(e.g. 15.)
-f            move to fourier domain
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

            elif arg == "-tap":
                width = float(argv.pop(0))
                options['prepro'].append(('-tap', width))

            elif arg == "-bp":
                fmin = float(argv.pop(0))
                fmax = float(argv.pop(0))
                order = float(argv.pop(0))
                options['prepro'].append(('-bp', fmin, fmax, order))

            elif arg == "-gbp":
                fcenter = float(argv.pop(0))
                alpha = float(argv.pop(0))
                options['prepro'].append(('-gbp', fcenter, alpha))

            elif arg == "-f":
                options['prepro'].append(('-f', ))

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

        elif cmd == "-tap":
            width = arg[1]
            for tr in st:
                tr.taperwidth(width)

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

        elif cmd == "-f":
            st = Stream([tr.to_fourier() for tr in st])

    if options['-v']:
        for tr in st:
            print(tr)

    return st

if __name__ == '__main__':

    npzfile, options = read_arguments()

    st = readseispystream(npzfile)
    st.sort_by('distance')

    st = prepro(st, options)

    import matplotlib.pyplot as plt

    if options['-m'] == 0:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for tr in st:
            tr: Trace
            # tr.obs(ax=plt.gca()
            tr.show(ax)
        plt.show()

    elif options['-m'] == 1:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        st.show(ax, gain=options['-g'], seedticks=True)
        plt.show()

    elif options['-m'] == 11:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        st.show(ax, gain=options['-g'], seedticks=True, obspy_decim=True)
        plt.show()

    elif options['-m'] == 2:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        st.shade(ax, powergain=options['-pg'], seedticks=True)
        plt.show()

    elif options['-m'] == 12:
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111)
        st.shade(ax, powergain=options['-pg'], cmap=plt.get_cmap("seismic"))
        st.show(ax, gain=options['-g'], seedticks=True)
        plt.show()

    else:
        raise NotImplementedError