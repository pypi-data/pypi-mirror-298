import socket
from mpi4py import MPI
 
# Multi-worker config
# We'll use mpi4py to figure out our rank, have each process select a socket and hostname,
# and allreduce that information to create a TF_CONFIG
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
hostname = socket.gethostname()

rank_info = {
    'rank': rank,
    'hostname': hostname,
}

rank_info_vector = comm.allgather(rank_info)

# Get the local rank
def get_local_rank(rank_info_vector):
    # Note that rank_info_vector is sorted by rank, by definition of the MPI allgather routine.
    # Thus, if our current rank is the n-th item in rank_info_vector for which the hostname matches,
    # our local rank is n
    local_rank = 0
    for item in rank_info_vector:
        if item['hostname'] == hostname:
            if item['rank'] == rank:
                return local_rank
            else:
                local_rank += 1

local_rank = get_local_rank(rank_info_vector)
MPI.Finalize()
print(local_rank)
