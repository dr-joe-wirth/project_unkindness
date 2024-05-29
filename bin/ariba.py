from bin.Parameters import Parameters
from Bio.SeqRecord import SeqRecord
import gzip, os, subprocess
from Bio.Seq import Seq
from Bio import SeqIO


def _ariba(params:Parameters) -> str:
    """runs ARIBA and processes the output

    Args:
        params (Parameters): a Parameters object

    Returns:
        str: the detected espW allele
    """
    aribaFn = __runAriba(params)


def _buildAribaDb(params:Parameters) -> None:
    """builds the ariba database using the values specified in a Parameters object

    Args:
        params (Parameters): a Parameters object
    """
    # constant
    ARIBA = "ariba"
    CMD = ("prepareref", "--all_coding", "no", "-f")
    
    # do not rebuild the database if it already exists
    if not os.path.exists(params._aribaDb):
        # build the command
        cmd = [ARIBA]
        cmd.extend(CMD)
        cmd.extend([params._referenceFna, params._aribaDb])

        # run the command
        subprocess.run(cmd, check=True, capture_output=True)


def __runAriba(params:Parameters) -> str:
    """runs ARIBA using the values specified in a Parameters object

    Args:
        params (Parameters): a Parameters object

    Returns:
        str: the file to be processed
    """
    # constants
    CMD = ("ariba", "run", "--threads")
    OUT_FN = "assembled_seqs.fa.gz"
    
    # determine the output directory
    params._aribaDir = os.path.join(params._aribaResultsDir, os.path.splitext(os.path.basename(params.reads[0]))[0][:-2])
  
    # build the command
    cmd = list(CMD)
    cmd.extend([str(params.threads), params._aribaDb, params.reads[0], params.reads[1], params._aribaDir])
    
    # run the command
    subprocess.run(cmd, check=True, capture_output=True)

    # return the file to be processed    
    return os.path.join(params._aribaDir, OUT_FN)
    

def __processAriba(aribaFn:str) -> str:
    pass
