import grpc
import bittorrent_pb2
import bittorrent_pb2_grpc

def download_file(stub):
    metadata = stub.RequestFileMetadata(bittorrent_pb2.Empty())
    file_size = metadata.size
    filename = metadata.filename

    with open(filename, 'wb') as f:
        for i in range((file_size + 1023) // 1024):
            request = bittorrent_pb2.FileChunkRequest(index=i)
            chunk = stub.RequestFileChunk(request)
            f.write(chunk.data)

    print(f"Downloaded file: {filename}")

def run_bittorrent_client():
    channel = grpc.insecure_channel('localhost:50051')
    bittorrent_stub = bittorrent_pb2_grpc.BitTorrentStub(channel)

    download_file(bittorrent_stub)

if __name__ == '__main__':
    run_bittorrent_client()