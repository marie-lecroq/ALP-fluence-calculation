from functions import *

import time
from mpi4py import MPI

# Set up the MPI environment and variables.
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
ncores = comm.Get_size()

# Define an output path.
path = "./"
verbosity_level = 0

# Define the grid of ALP masses log10(m/eV) and coupling log10(g/GeV^-1) and their combination.
logm = np.arange(3,9,0.05)
logg = np.arange(-13,-3,0.05)
pairs = np.array(np.meshgrid(logm, logg)).T.reshape(-1,2)
ntasks = len(pairs)

# The container for the result
res = np.zeros(3)


start_time = time.time()
# Let the workers calculate the flux.
if (rank > 0):
    # Send dummy result to master to signal that this process is ready for work.
    comm.Send(res, dest=0)
    for i in range(1, ntasks+1):
        id = comm.recv(source=0)
        if (id > ntasks):
            break
        lgm, lgg = pairs[id]
        res = expected_photon_fluence(10**lgm,10**(lgg-9.0),vebosity_level)
        comm.Send(res, dest= 0)
    print('MPI rank {} finished! MC simulations took {:.1f} mins.'.format( rank, (time.time()-start_time)/60.0 ))

# Let the master process distribute tasks and receive results:
if (rank == 0):
    all_results = []
    stat = MPI.Status()
    for task_id in range(1, ntasks+ncores):
        comm.Recv(res, source=MPI.ANY_SOURCE, status=stat)
        all_results.append(res)
        worker_id = stat.Get_source()
        comm.send(task_id, dest=worker_id)
    print('All MPI tasks finished after {:.1f} mins!'.format( rank, (time.time()-start_time)/60.0 ))

    start_io_time = time.time()
    out_file_name = path+"SN1987A_DecayFluence.dat"
    print('Formatting results and saving them to '+out_file_name+'.')
    a = np.array(all_results)
    a = a[a[:,1].argsort()]
    a = a[a[:,0].argsort(kind='mergesort')]
    header_string = "Fluence of SN1987A photons from axion decay\nMC simulations by Marie Lecroq, Sebastian Hoof, and Csaba Balazs based on arXiv:1702.02964\nColumns: Value of log10(m/eV) | Value of log10(g/GeV^-1) | Fluence value in cm^-2"
    np.savetxt(path+"SN1987A_DecayFluence.dat", a, fmt="%.3f %.3f %.10e", header=header_string, comments="# ")
    print('Formatting and saving file took {:.2f} mins!'.format( (time.time()-start_io_time)/60.0 ))
    print('All tasks complete! Finishing MPI routine now.')
