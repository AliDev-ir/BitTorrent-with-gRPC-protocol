import grpc
from concurrent import futures
import bittorrent_pb2
import bittorrent_pb2_grpc

class BitTorrentServicer(bittorrent_pb2_grpc.BitTorrentServicer):
    def __init__(self):
        self.file_data = b"Hello"

    def RequestFileMetadata(self, request, context):
        return bittorrent_pb2.FileMetadata(filename="sample.txt", size=len(self.file_data))

    def RequestFileChunk(self, request, context):
        start = request.index * 1024
        end = start + 1024
        chunk_data = self.file_data[start:end]
        return bittorrent_pb2.FileChunk(index=request.index, data=chunk_data)

    def UploadFileChunk(self, request, context):
        print(f"Received chunk {request.index}")
        return bittorrent_pb2.Empty()

def run_bittorrent_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bittorrent_pb2_grpc.add_BitTorrentServicer_to_server(BitTorrentServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    run_bittorrent_server()
