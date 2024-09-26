import argparse

from . import Server

def run_server():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-P", "--port", type=int, help="The port number.")
    args = parser.parse_args()

    server = Server()
    server.port = args.port
    server.run()
    
