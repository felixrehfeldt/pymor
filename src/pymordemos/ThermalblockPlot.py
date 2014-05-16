'''ThermalblockPlot demo.

Usage:
  ThermalblockPlot.py [-ehp] [--estimator-norm=NORM] [--extension-alg=ALG] [--grid=NI] [--help]
                  [--plot-solutions] [--plot-error-sequence] [--reductor=RED] [--test=COUNT]
                  XBLOCKS YBLOCKS SNAPSHOTS RBSIZE


Arguments:
  XBLOCKS    Number of blocks in x direction. 4-Array

  YBLOCKS    Number of blocks in y direction. 4-Array

  SNAPSHOTS  Number of snapshots for basis generation per component.
             In total SNAPSHOTS^(XBLOCKS * YBLOCKS).

  RBSIZE     Size of the reduced basis


Options:
  -e, --with-estimator   Use error estimator.

  --estimator-norm=NORM  Norm (trivial, h1) in which to calculate the residual
                         [default: trivial].

  --extension-alg=ALG    Basis extension algorithm (trivial, gram_schmidt, h1_gram_schmidt)
                         to be used [default: h1_gram_schmidt].

  --grid=NI              Use grid with 2*NI*NI elements [default: 100].

  -h, --help             Show this message.

  -p, --plot-err         Plot error.

  --plot-solutions       Plot some example solutions.

  --test=COUNT           Use COUNT snapshots for stochastic error estimation
                         [default: 10].

'''

from __future__ import absolute_import, division, print_function

__author__ = 'f_rehf02'


from docopt import docopt
from pymordemos.thermalblock import thermalblock_demo
import numpy as np


if __name__ == '__main__':
    # parse arguments
    args = docopt(__doc__)

    # run demo
    args['XBLOCKS'] = '1'
    args['YBLOCKS'] = '4'
    tmp_err_list, tmp_est_list, tmp_cond_list = thermalblock_demo(args)
    i = 0;
    savedtextstring = 'size,err,est,cond\n'
    for err, est, cond in zip(tmp_err_list, tmp_est_list, tmp_cond_list):
            savedtextstring += str(i+1) + ',' + str(err) + ',' + str(est[0]) + ',' + str(cond) + '\n'
            i += 1
    DAT = np.column_stack(savedtextstring)
    np.savetxt('data/data1.txt',DAT, delimiter='', fmt = '%s')

    args['XBLOCKS'] = '2'
    args['YBLOCKS'] = '5'
    tmp_err_list, tmp_est_list, tmp_cond_list = thermalblock_demo(args)
    i = 0;
    savedtextstring = 'size,err,est,cond\n'
    for err, est, cond in zip(tmp_err_list, tmp_est_list, tmp_cond_list):
            savedtextstring +=  str(i+1) + ',' + str(err) + ',' + str(est[0]) + ',' + str(cond) + '\n'
            i += 1
    DAT = np.column_stack(savedtextstring)
    np.savetxt('data/data2.txt',DAT, delimiter='', fmt = '%s')

    args['XBLOCKS'] = '2'
    args['YBLOCKS'] = '2'
    tmp_err_list, tmp_est_list, tmp_cond_list = thermalblock_demo(args)
    i = 0;
    savedtextstring = 'size,err,est,cond\n'
    for err, est, cond in zip(tmp_err_list, tmp_est_list, tmp_cond_list):
            savedtextstring +=  str(i+1) + ',' + str(err) + ',' + str(est[0]) + ',' + str(cond) + '\n'
            i += 1
    DAT = np.column_stack(savedtextstring)
    np.savetxt('data/data3.txt',DAT, delimiter='', fmt = '%s')

    args['XBLOCKS'] = '3'
    args['YBLOCKS'] = '1'
    tmp_err_list, tmp_est_list, tmp_cond_list = thermalblock_demo(args)
    i = 0;
    savedtextstring = 'size,err,est,cond\n'
    for err, est, cond in zip(tmp_err_list, tmp_est_list, tmp_cond_list):
            savedtextstring +=  str(i+1) + ',' + str(err) + ',' + str(est[0]) + ',' + str(cond) + '\n'
            i += 1
    DAT = np.column_stack(savedtextstring)
    np.savetxt('data/data4.txt',DAT, delimiter='', fmt = '%s')

    DAT = np.column_stack(savedtextstring)
    print(savedtextstring)
