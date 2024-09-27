import json
import socket
from contextlib import closing

from mpi4py import MPI

def find_free_port():
    with closing(socket.socket()) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        return s.getsockname()[1]

# Multi-worker config
# We'll use mpi4py to figure out our rank, have each process select a socket and hostname,
# and allreduce that information to create a TF_CONFIG
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
hostname = socket.gethostname()
port = find_free_port()

rank_info = {
    'rank': rank,
    'hostname': hostname,
    'port': port,
}

rank_info_vector = comm.allgather(rank_info)

worker_list = ['%s:%s' % (item['hostname'], item['port']) for item in rank_info_vector]

tf_config = {
    'cluster': {
        'worker': worker_list,
    },
    'task': {'type': 'worker', 'index': rank}
}

MPI.finalize()
print(json.dumps(tf_config))
