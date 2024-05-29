from bin.Parameters import Parameters
from bin.BlastHit import BlastHit
import os, subprocess


def _blastn(params:Parameters):
    """runs BLASTn to detect espW alleles using the values specified in a Parameters object

    Args:
        params (Parameters): a Parameters object
    """
    __makeBlastDb(params)
    __runBlast(params)


def __makeBlastDb(params:Parameters) -> None:
    """makes a blastn database for the input genome using the values specified in a Parameters object

    Args:
        params (Parameters): a Parameters object
    """
    # constants
    CMD_A = "makeblastdb"
    CMD_B = ("-dbtype", "nucl", "-out")
    
    # get the blast db name
    params._blastDb = os.path.join(params._blastDbDir, os.path.splitext(os.path.basename(params.fna))[0])
    
    # build the command
    cmd = [CMD_A]
    cmd.extend(CMD_B)
    cmd.extend([params._blastDb, "-in", params.fna])
    
    # make the blastdb
    subprocess.run(cmd, check=True, capture_output=True)


def __runBlast(params:Parameters) -> None:
    """runs blastn using the values specified in a Parameters object

    Args:
        params (Parameters): a Parameters object
    """
    # constants
    FN_SUFFIX = f"_vs_{os.path.basename(os.path.splitext(params._referenceFna)[0])}.blastn"
    BLASTN = "blastn"
    CMD = ("-max_target_seqs", "10000",
           "-outfmt", '6 qseqid sseqid length qstart qend sstart send qcovhsp pident')
    
    # determine the output file
    params._blastFn = os.path.join(params._blastResultsDir, os.path.splitext(os.path.basename(params.fna))[0] + FN_SUFFIX)
    
    # build the blastn command
    cmd = [BLASTN]
    cmd.extend(CMD)
    cmd.extend(["-query", params._referenceFna])
    cmd.extend(['-db', params._blastDb])
    cmd.extend(['-perc_identity', str(params._blastPid)])
    cmd.extend(['-qcov_hsp_perc', str(params._blastQcov)])
    cmd.extend(['-num_threads', str(params.threads)])
    cmd.extend(['-out', params._blastFn])
    
    if params._blastUngapped:
        cmd.append("-ungapped")
    
    # run blastn
    subprocess.run(cmd, check=True, capture_output=True)


def __parseBlastTable(fn:str) -> tuple[str,str]:
    pass
