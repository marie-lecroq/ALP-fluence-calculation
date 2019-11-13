from functions import *

#from tqdm import tqdm
import time
from mpi4py import MPI

# Retrieve MPI environment and variables:
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
ncores = comm.Get_size()

path = "./"

# Define the grid of ALP masses log10(m/eV) and coupling log10(g/GeV^-1):
logm = np.arange(3,9,0.05)
logg = np.arange(-13,-3,0.05)

# Define partition that spreads jobs evenly across the grid; this should be better for many MPI processes:
pairs = np.array(np.meshgrid(logm, logg)).T.reshape(-1,2)
min_size, extras = divmod(len(pairs), ncores)
partition = [[pairs[ncores*j+i] for j in range(min_size+(i<extras))] for i in range(ncores)]
local_partition = partition[rank]
# Block-like partition
#partition = np.array_split(pairs,ncores)
#local_partition = partition[rank]

local_results = []
start_time = time.time()
for lgm, lgg in local_partition:
    # Here, just get the result. Use the alternative function to save intermediate results.
    res = expected_photon_fluence(10**lgm,10**(lgg-9.0))
    #print('{:.3f} {:7.3f} {:.10e}'.format(lgm,lgg,res))
    local_results.append(res)
print('MPI rank {} finished! MC simulations took {:.1f} mins.'.format( rank, (time.time()-start_time)/60.0 ))

# Local send buffer for all results:
sendbuf = np.array(local_results)
# Tell MPI how many results to get from each process:
sizes = comm.gather(len(sendbuf), root=0)
#displacements = [int(sum(sizes[:i])) for i in range(len(sizes))]
# Local send buffers
recvbuf = None
if rank == 0:
    recvbuf = np.empty(sum(sizes), dtype=np.float64)

# Receive results on the 0 process:
comm.Gatherv(sendbuf=sendbuf, recvbuf=(recvbuf, sizes), root=0)
# N.B.: undocumented feature; recvbuf missing arguments displacement is inferred from sendcounts and type from recvbuf.
#       Full signature is comm.Gatherv(sendbuf=sendbuf, recvbuf=[recvbuf, (sizes, displacements), MPI.DOUBLE], root=0).

# Combine results on rank 0:
if rank == 0:
    print("Combining all results...")
    start_time = time.time()

    flat_partition = [item for sublist in partition for item in sublist]
    a = np.array([[flat_partition[i][0],flat_partition[i][1],res] for i,res in enumerate(recvbuf)])
    # Sort results according to mass and then coupling
    a = a[a[:,1].argsort()]
    a = a[a[:,0].argsort(kind='mergesort')]
    header_string = "Fluence of SN1987A photons from axion decay\nMC simulations by Marie Lecroq, Sebastian Hoof, and Csaba Balazs based on arXiv:1702.02964\nColumns: Value of log10(m/eV) | Value of log10(g/GeV^-1) | Fluence value in cm^-2"
    # Save full results to text file:
    np.savetxt("./SN1987A_DecayFluence.dat", a, fmt="%.3f %.3f %.10e", header=header_string, comments="# ")

    print('Combination complete after {:.2f} mins!'.format( (time.time()-start_time)/60.0 ))
