import argparse
import numpy as np
from uncertainties import ufloat
import lib_topology as es
import pickle as pkl

parser = argparse.ArgumentParser()
parser.add_argument("TE", type=float)
parser.add_argument("WE", type=float)
parser.add_argument("input_datafiles", nargs="+")
parser.add_argument("--group", type=str, default="SPN")
parser.add_argument("--output_data", type=argparse.FileType("w"), default="-")
parser.add_argument("--output_tex", type=argparse.FileType("w"), default="-")
parser.add_argument("--sqrt_sigma_filename", default="./sqrts_vs_beta.dat")
parser.add_argument("--num_bs", type=int, default=es.DEFAULT_NUM_BS)
parser.add_argument("--pickle_dir", default="pkl_flows_bs")
args = parser.parse_args()

for fname in args.input_datafiles:
    iN, iL, iB, rawdata = es.topo_load_raw_data(fname)
    if args.group == "SPN":
        TE_scaled = args.TE * es.Casimir_SP(iN)
        WE_scaled = args.WE * es.Casimir_SP(iN)
    elif args.group == "SUN":
        TE_scaled = args.TE * es.Casimir_SUN(iN)
        WE_scaled = args.WE * es.Casimir_SUN(iN)
    else:
        TE_scaled = args.TE
        WE_scaled = args.WE 
    fn_bs = args.pickle_dir + "/pkl_bs_" + iN + "_" + iL + "_" + iB + "_"
    infile = open(fn_bs + "t_E", "rb")
    bs_flow_E = pkl.load(infile)
    infile.close()
    infile = open(fn_bs + "w_E", "rb")
    w0_flow_E = pkl.load(infile)
    infile.close()
    infile = open(fn_bs + "t_symE", "rb")
    bs_flow_symE = pkl.load(infile)
    infile.close()
    infile = open(fn_bs + "w_symE", "rb")
    w0_flow_symE = pkl.load(infile)
    infile.close()

    t0_tmp_symE = es.find_t0(bs_flow_symE, TE_scaled,  num_bs=args.num_bs) #rng=tw_rng,
    t0_tmp_E = es.find_t0(bs_flow_E, TE_scaled,  num_bs=args.num_bs) #rng=tw_rng,

    w0_tmp_symE = es.find_w0(w0_flow_symE, WE_scaled, num_bs=args.num_bs) #rng=tw_rng, 
    w0_tmp_E = es.find_w0(w0_flow_E, WE_scaled, num_bs=args.num_bs)
    print(
        iN,
        iB,
        TE_scaled,
        t0_tmp_E[0],
        t0_tmp_E[1],
        t0_tmp_symE[0],
        t0_tmp_symE[1],
        WE_scaled,
        w0_tmp_E[0],
        w0_tmp_E[1],
        w0_tmp_symE[0],
        w0_tmp_symE[1],
        file=args.output_data,
    )


