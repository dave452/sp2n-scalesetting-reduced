PROD_DIR="raw_data/ScaleSetting/"
TMP_DIR="tmp/ScaleSetting/"
WF_RESULTS="extern_data/Sp4_w0.dat"
create_WF_files.sh $PROC_DIR $TMP_DIR
NUM_BS=50
PICKLE_DIR="$TMP_DIR"/pickle_files/
E0=0.6
W0=0.6
for f in "$TMP_DIR"/WF*; do
    python produce_bs_sample.py $f --num_bs $NUM_BS --pickle_dir $PICKLE_DIR
done
python Topology.py $E0 $W0 "$TMP_DIR"/WF* --pickle_dir $PICKLE_DIR --group "SPN" > $WF_RESULTS
